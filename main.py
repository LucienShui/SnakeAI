from __future__ import absolute_import, print_function

import argparse


def get_or_default(item, default):
    if item is None:
        return default
    return item


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    # parser.add_argument('--human', help='human play', action='store_true')
    # parser.add_argument('train', help='train agent')
    # parser.add_argument('--render', help='render game', action='store_true')
    parser.add_argument('--shape', help='game size, default is 4 4', nargs=2, type=int, default=[4, 4])
    # parser.add_argument('--episode', help='training episode, default is inf', type=int, default=None)
    # parser.add_argument('--frame-size', help='frame size, default is 1', type=int, default=1)
    # parser.add_argument('--log-level', help='DEBUG, INFO, WARNING, ERROR, CRITICAL, default is INFO', type=str)
    # parser.add_argument('--model-path', help='path of model', type=str)

    sub_parsers = parser.add_subparsers(title='player')
    sub_parsers.required = True
    sub_parsers.dest = 'player'

    agent_parser = sub_parsers.add_parser('agent', parents=[parser],
                                          add_help=False, help='play with agent')
    human_parser = sub_parsers.add_parser('human', parents=[parser],
                                          add_help=False, help='play manually')
    human_parser.add_argument_group()

    agent_sub_parsers = agent_parser.add_subparsers(title='type')
    agent_sub_parsers.required = True
    agent_sub_parsers.dest = 'type'

    play_parser = agent_sub_parsers.add_parser('play', parents=[agent_parser],
                                               add_help=False, help='play without training')

    # train_parser = sub_parsers.add_parser('train', parents=[parser], add_help=False)

    args = parser.parse_args()
    human_args = human_parser.parse_args()
    agent_args = agent_parser.parse_args()
    play_args = play_parser.parse_args()

    print(args)
    print(human_args)
    print(agent_args)
    exit(0)

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
