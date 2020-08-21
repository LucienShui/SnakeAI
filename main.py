from __future__ import absolute_import, print_function

import logging
import curses
import re
import sys

from agent import DeepQLearningNetwork
from graphic import CursesSnake
from gym.envs import SnakeEnv

logger: logging.Logger = logging.getLogger('main')
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def custom_reward(info: dict) -> float:
    snake_x = info['bodies'][0]['x']
    snake_y = info['bodies'][0]['y']

    apple_x = info['apple']['x']
    apple_y = info['apple']['y']

    return (1 / (abs(snake_x - apple_x) + abs(snake_y - apple_y))) * .5


def agent_play(shape: tuple, render: bool = False, training: bool = False):
    logger.debug('create env start')
    env = SnakeEnv(shape)
    logger.debug('create env finished')

    logger.debug('create dqn start')
    dqn = DeepQLearningNetwork(shape,
                               len(env.action_space),
                               initial_epsilon=.0,
                               batch_size=32,
                               queue_size=1 << 8)
    logger.debug('create dqn finished')

    if not training:
        dqn.load_model('model.h5')

    best_score: int = 0

    for i_episode in range(2000):
        observation = env.reset()
        for t in range(1000):
            if render:
                env.render()
            action = dqn.greedy_action(observation) if training else dqn.action(observation)
            next_observation, reward, done, info = env.step(action)

            if training:
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

    if training:
        dqn.save('model.h5')


def main():
    logger.debug('main() start')

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

    logger.debug(f'shape = {shape}, human = {human}, render = {render}, training = {training}')

    if human:
        def temp_func(screen):
            CursesSnake(screen, shape).run()

        curses.wrapper(temp_func)
    else:
        agent_play(shape, render=render, training=training)


if __name__ == '__main__':
    main()
