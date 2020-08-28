from __future__ import absolute_import, print_function

import argparse

from agent import Agent
from graphic import CursesSnake


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--human', help='human play', action='store_true')
    parser.add_argument('--training', help='training dqn', action='store_true')
    parser.add_argument('--render', help='render game', action='store_true')
    parser.add_argument('--shape', help='game size, default is 4 4', nargs=2, type=int)
    parser.add_argument('--episode', help='training episode, default is inf', type=int)
    parser.add_argument('--log-level', help='DEBUG, INFO, WARNING, ERROR, CRITICAL, default is INFO', type=str)

    args = parser.parse_args()

    args.shape = (4, 4) if args.shape is None else tuple(args.shape)
    args.log_level = 'INFO' if args.log_level is None else args.log_level

    return args


def distance_reward(info: dict) -> float:
    snake_x = info['bodies'][0]['x']
    snake_y = info['bodies'][0]['y']

    apple_x = info['apple']['x']
    apple_y = info['apple']['y']

    return (1 / (abs(snake_x - apple_x) + abs(snake_y - apple_y))) * .5


def main():
    args = get_args()

    if args.human:
        CursesSnake(args.shape).run()
    else:
        agent: Agent = Agent(args.shape, render=args.render, episode=args.episode, logger_level=args.log_level)
        if args.training:
            agent.train()
        else:
            agent.play()


if __name__ == '__main__':
    main()
