from __future__ import absolute_import, print_function

import re
import sys
import queue
import time

from agent import DeepQNetwork
from graphic import CursesSnake
from gym.envs import SnakeEnv


def distance_reward(info: dict) -> float:
    snake_x = info['bodies'][0]['x']
    snake_y = info['bodies'][0]['y']

    apple_x = info['apple']['x']
    apple_y = info['apple']['y']

    return (1 / (abs(snake_x - apple_x) + abs(snake_y - apple_y))) * .5


def agent_play(shape: tuple, render: bool = False):
    env = SnakeEnv(shape)

    dqn = DeepQNetwork(shape,
                       len(env.action_space),
                       initial_epsilon=.9,
                       batch_size=32,
                       queue_size=1 << 8)

    dqn.load_model('model.h5')

    observation = env.reset()
    while True:
        if render:
            env.render()
        action = dqn.action(observation)
        next_observation, reward, done, info = env.step(action)

        observation = next_observation
        if done:
            break

        time.sleep(50 / 1000)

    env.close()


def train(shape: tuple, render: bool = False):
    env = SnakeEnv(shape)

    dqn = DeepQNetwork(shape,
                       len(env.action_space),
                       initial_epsilon=.0,
                       batch_size=32,
                       queue_size=1 << 8)

    best_score: int = 0

    for i_episode in range(2000):
        observation = env.reset()
        action_cnt: int = 0
        action_queue: queue.Queue = queue.Queue()
        for t in range(1000):
            if render:
                env.render()
            action = dqn.greedy_action(observation)

            next_observation, reward, done, info = env.step(action)
            action_cnt = 0 if reward > 0 else action_cnt + 1

            def custom_reward() -> (float, done):

                # 如果原地转圈则提前结束并惩罚
                action_queue.put(action)
                while action_queue.qsize() > 4:
                    action_queue.get()

                if action_queue.qsize() == 4 and set(action_queue.queue).__len__() == 1 and action_queue.queue[0] != 0:
                    return -10, True

                # 如果无用步数过多则提前结束并惩罚
                if action_cnt > shape[0] * shape[1] * 2:
                    return -10, True

                return reward, done

            reward, done = custom_reward()

            # 记录并学习
            dqn.fit(observation, reward, done, action, next_observation)

            observation = next_observation
            if done:
                best_score = max(best_score, env.curses_snake.snake.length)
                if (i_episode + 1) % 100 == 0:
                    dqn.save('model.h5')
                    print("Episode {} finished after {} time steps, best score is {}".format(
                        i_episode + 1, t + 1, best_score))
                break
    env.close()

    dqn.save('model.h5')


def main():
    config = {
        'shape': '(9, 9)',
        'human': 'false',
        'render': 'false',
        'training': 'false'
    }

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            key, value = sys.argv[i].split('=')
            config[key[2:]] = value

    shape: tuple = tuple(map(int, re.findall(r'\d+', config['shape'])))
    human: bool = config['human'][0] in ['t', '1']
    render: bool = config['render'][0] in ['t', '1']
    training: bool = config['training'][0] in ['t', '1']

    if human:
        CursesSnake(shape).run()
    elif training:
        train(shape, render=render)
    else:
        agent_play(shape, render=render)


if __name__ == '__main__':
    main()
