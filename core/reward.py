from __future__ import absolute_import, print_function

from enum import Enum


class Reward(Enum):
    DEATH = -100
    ACTION = -1
    APPLE = 10
    WIN = 100
