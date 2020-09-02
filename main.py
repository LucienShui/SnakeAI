from __future__ import absolute_import, print_function

import argparse


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--human', help='human play', action='store_true')
    parser.add_argument('--training', help='training dqn', action='store_true')
    parser.add_argument('--render', help='render game', action='store_true')
    parser.add_argument('--shape', help='game size, default is 10 10', nargs=2, type=int, default=[10, 10])
    parser.add_argument('--episode', help='training episode, default is inf', type=int)
    parser.add_argument('--frame-size', help='frame size, default is 1', type=int, default=1)
    parser.add_argument('--log-level', type=str, default='info',
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='debug, info, warning, error, critical, default is info')

    args = parser.parse_args()

    args.log_level = args.log_level.upper()
    args.shape = tuple(args.shape)

    return args


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
