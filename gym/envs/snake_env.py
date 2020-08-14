from __future__ import absolute_import, print_function

import typing

import numpy

import gym
from graphic import CursesSnake


class SnakeEnv(gym.Env):
    """
    0 -> go straight
    1 -> turn left
    2 -> turn right
    """
    action_space = numpy.array([0, 1, 2])

    def __init__(self, shape: [typing.List[int], typing.Tuple[int, int]] = (4, 4)):
        self.shape = shape
        self.curses_snake: CursesSnake = CursesSnake(self.shape)

        game_action_space = self.curses_snake.snake.action_space

        self.direction_env_action_to_game_action: typing.Dict[int, typing.List[int]] = {
            game_action_space.UP: [game_action_space.NONE, game_action_space.LEFT, game_action_space.RIGHT],
            game_action_space.DOWN: [game_action_space.NONE, game_action_space.RIGHT, game_action_space.LEFT],
            game_action_space.LEFT: [game_action_space.NONE, game_action_space.DOWN, game_action_space.UP],
            game_action_space.RIGHT: [game_action_space.NONE, game_action_space.UP, game_action_space.DOWN]
        }

    def reset(self) -> typing.List[typing.List[int]]:
        self.curses_snake = CursesSnake(self.shape)
        return self.curses_snake.snake.game_board.data

    def render(self, mode='human') -> None:
        self.curses_snake.render()

    def step(self, action: int) -> (typing.List[typing.List[int]], int, bool, typing.Any):
        return self.curses_snake.snake.step(
            self.direction_env_action_to_game_action[
                self.curses_snake.snake.snake.direction][action])

    def close(self):
        self.curses_snake.close()

    def seed(self, seed=None):
        pass
