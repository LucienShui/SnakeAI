from __future__ import absolute_import, print_function

import typing
import logging

import gym
from core import Action
from graphic import CursesSnake


class SnakeEnv(gym.Env):
    """
    0 -> go straight
    1 -> turn left
    2 -> turn right
    """
    action_space = [0, 1, 2]

    def __init__(self, screen=None, shape: [typing.List[int], typing.Tuple[int, int]] = (4, 4)):
        kwargs = locals()

        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.debug(f'init with kwargs = {kwargs}')

        self.screen = screen
        self.shape = shape
        self.curses_snake: CursesSnake = ...

        action_space = Action
        up, down, left, right, none = (action_space.UP, action_space.DOWN, action_space.LEFT,
                                       action_space.RIGHT, action_space.NONE)

        self.direction_env_action_to_game_action: typing.Dict[int, typing.List[int]] = {
            up: [none, left, right],
            down: [none, right, left],
            left: [none, down, up],
            right: [none, up, down]
        }
        self.reset()
        self.logger.debug('init finished')

    def reset(self) -> typing.List[typing.List[int]]:
        self.curses_snake = CursesSnake(self.screen, self.shape)
        return self.curses_snake.snake.game_board.data

    def render(self, mode='human') -> None:
        self.curses_snake.render()

    def step(self, action: int) -> (typing.List[typing.List[int]], float, bool, typing.Any):
        return self.curses_snake.snake.step(
            self.direction_env_action_to_game_action[
                self.curses_snake.snake.snake.direction][action])

    def close(self):
        self.curses_snake.close()

    def seed(self, seed=None):
        pass
