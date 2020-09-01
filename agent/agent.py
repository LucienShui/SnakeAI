from __future__ import absolute_import, print_function

import logging
import queue
import time

from core import Reward
from dqn import DeepQNetworkWithDrop as DeepQNetwork
from dqn.param import Param
from gym.envs import SnakeEnv


class Agent(object):

    def __init__(self, shape: tuple,
                 render: bool = False,
                 episode: int = None,
                 model_path: str = 'model.h5',
                 logger_level: str = 'INFO'):
        logging.basicConfig()
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logger_level)

        self.model_path: str = model_path
        self.shape: tuple = shape
        self.episode: int = episode
        self.render: bool = render

        self.env = SnakeEnv(shape)

        self.dqn = DeepQNetwork(shape, len(self.env.action_space), gamma=Param.GAMMA,
                                buffer_size=Param.BUFFER_SIZE, batch_size=Param.BATCH_SIZE,
                                initial_epsilon=Param.INITIAL_EPSILON, epsilon_decay=Param.EPSILON_DECAY,
                                final_epsilon=Param.FINAL_EPSILON, learning_rate=Param.LEARNING_RATE)

    def play(self):
        self.dqn.load_model(self.model_path)

        observation = self.env.reset()
        if self.render:
            self.env.render()

        while True:
            time.sleep(1000 / 1000)

            action = self.dqn.action(observation)
            next_observation, reward, done, info = self.env.step(action)

            if self.render:
                self.env.render()

            observation = next_observation
            if done:
                break

        self.env.close()

    def custom_reward(self, action: int, reward: float, done: bool,
                      action_queue: queue.Queue, action_cnt_without_apple: int) -> (float, bool):

        # 如果原地转圈则惩罚
        action_queue.put(action)
        while action_queue.qsize() > 4:
            action_queue.get()

        if action_queue.qsize() == 4 and set(action_queue.queue).__len__() == 1 and action_queue.queue[0] != 0:
            return Reward.SAME_ACTION, True

        # 如果无用步数过多则提前结束并惩罚
        if action_cnt_without_apple > self.shape[0] * self.shape[1] * 2:
            return Reward.TOO_MANY_ACTION, True

        return reward, done

    def train_step(self) -> (int, float):
        """
        单轮游戏中进行训练
        :return: 本轮游戏分数，本轮 reward 总和，本轮操作次数
        """
        observation = self.env.reset()
        action_cnt_without_apple: int = 0  # 操作次数累加器，在吃到果子时清零
        action_queue: queue.Queue = queue.Queue()
        reward_sum: int = 0  # 本轮 reward 总和
        action_cnt: int = 0  # 操作次数累加器

        for t in range(1 << 11):
            if self.render:
                self.env.render()
            action = self.dqn.greedy_action(observation)

            next_observation, reward, done, info = self.env.step(action)
            action_cnt_without_apple = 0 if reward > 0 else action_cnt_without_apple + 1

            reward, done = self.custom_reward(action, reward, done, action_queue, action_cnt_without_apple)

            action_cnt += 1
            reward_sum += reward

            # 记录并学习
            self.dqn.fit(observation, reward, done, action, next_observation)

            observation = next_observation
            if done:
                break
        return self.env.curses_snake.snake.length, reward_sum, action_cnt

    def train(self):

        best_score: int = 0
        score_sum: int = 0
        reward_sum: int = 0
        action_cnt: int = 0
        i_episode = 0

        while True:
            buf_score, buf_reward_sum, buf_action_cnt = self.train_step()

            score_sum += buf_score
            reward_sum += buf_reward_sum
            action_cnt += buf_action_cnt
            best_score = max(best_score, buf_score)
            i_episode += 1

            self.logger.debug(f'i_episode = {i_episode}, '
                              f'score = {buf_score}, '
                              f'epsilon = {self.dqn.epsilon}, '
                              f'average_reward = {buf_reward_sum / buf_action_cnt}')

            if i_episode % 100 == 0:
                self.dqn.save(self.model_path)
                self.logger.info(f'i_episode = {i_episode}, '
                                 f'epsilon = {self.dqn.epsilon}, '
                                 f'average_reward = {reward_sum / action_cnt}, '
                                 f'average_score = {score_sum / i_episode}, '
                                 f'best_score = {best_score}')

            if self.episode is not None and i_episode > self.episode:
                break

        self.env.close()

        self.dqn.save(self.model_path)
