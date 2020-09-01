from __future__ import absolute_import, print_function

import argparse


def get_or_default(item, default):
    if item is None:
        return default
    return item


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--human', help='human play', action='store_true')
    parser.add_argument('--training', help='training dqn', action='store_true')
    parser.add_argument('--render', help='render game', action='store_true')
    parser.add_argument('--shape', help='game size, default is 4 4', nargs=2, type=int)
    parser.add_argument('--episode', help='training episode, default is inf', type=int)
    parser.add_argument('--frame-size', help='frame size, default is 1', type=int)
    parser.add_argument('--log-level', help='DEBUG, INFO, WARNING, ERROR, CRITICAL, default is INFO', type=str)

    args = parser.parse_args()

    args.shape = tuple(get_or_default(args.shape, (4, 4)))
    args.frame_size = get_or_default(args.frame_size, 1)
    args.log_level = get_or_default(args.log_level, 'INFO').upper()

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
        from graphic import CursesSnake

        CursesSnake(args.shape).run()

    else:
        from agent import Agent

        agent: Agent = Agent(args.shape, render=args.render, episode=args.episode,
                             logger_level=args.log_level, frame_size=args.frame_size)
        if args.training:
            agent.train()
        else:
            agent.play()


if __name__ == '__main__':
    main()
