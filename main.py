from __future__ import absolute_import, print_function

import argparse
import logging
import queue
import time

from agent import DeepQNetwork
from graphic import CursesSnake
from gym.envs import SnakeEnv

logging.basicConfig(level=logging.INFO)


def distance_reward(info: dict) -> float:
    snake_x = info['bodies'][0]['x']
    snake_y = info['bodies'][0]['y']

    apple_x = info['apple']['x']
    apple_y = info['apple']['y']

    return (1 / (abs(snake_x - apple_x) + abs(snake_y - apple_y))) * .5


def agent_play(shape: tuple, render: bool = False):
    env = SnakeEnv(shape)

    dqn = DeepQNetwork(shape, len(env.action_space))

    dqn.load_model('model.h5')

    observation = env.reset()
    if render:
        env.render()

    while True:
        action = dqn.action(observation)
        next_observation, reward, done, info = env.step(action)

        if render:
            env.render()

        observation = next_observation
        if done:
            break

        time.sleep(1000 / 1000)

    env.close()


def train_step(shape: tuple, env: SnakeEnv, dqn: DeepQNetwork, render: bool = False) -> int:
    observation = env.reset()
    action_cnt: int = 0
    action_queue: queue.Queue = queue.Queue()
    for t in range(1 << 11):
        if render:
            env.render()
        action = dqn.greedy_action(observation)

        next_observation, reward, done, info = env.step(action)
        action_cnt = 0 if reward > 0 else action_cnt + 1

        def custom_reward() -> (float, done):

            # 如果原地转圈则惩罚
            action_queue.put(action)
            while action_queue.qsize() > 4:
                action_queue.get()

            if action_queue.qsize() == 4 and set(action_queue.queue).__len__() == 1 and action_queue.queue[0] != 0:
                return -1, done

            # 如果无用步数过多则提前结束并惩罚
            if action_cnt > shape[0] * shape[1] * 2:
                return -1, True

            return reward, done

        reward, done = custom_reward()

        # 记录并学习
        dqn.fit(observation, reward, done, action, next_observation)

        observation = next_observation
        if done:
            break
    return env.curses_snake.snake.length


def train(shape: tuple, render: bool = False, episode: int = 2048):
    env = SnakeEnv(shape)

    dqn = DeepQNetwork(shape, len(env.action_space), initial_epsilon=2)

    best_score: int = 0

    i_episode = 0

    while True:
        best_score = max(best_score, train_step(shape, env, dqn, render=render))
        i_episode += 1

        if i_episode % 100 == 0:
            dqn.save('model.h5')
            print(f"Episode {i_episode} finished, epsilon = {dqn.epsilon}, best score is {best_score}")

        if episode is not None and i_episode > episode:
            break

    env.close()

    dqn.save('model.h5')


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--human', help='human play', action='store_true')
    parser.add_argument('--training', help='training agent', action='store_true')
    parser.add_argument('--render', help='render game', action='store_true')
    parser.add_argument('--shape', help='game size', nargs=2, type=int)
    parser.add_argument('--episode', help='training episode', type=int)

    args = parser.parse_args()

    args.shape = (4, 4) if args.shape is None else tuple(args.shape)

    return args


def main():
    args = get_args()

    if args.human:
        CursesSnake(args.shape).run()
    elif args.training:
        train(args.shape, render=args.render, episode=args.episode)
    else:
        agent_play(args.shape, render=args.render)


if __name__ == '__main__':
    main()
