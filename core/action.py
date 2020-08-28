from __future__ import absolute_import, print_function


class Action(object):
    UP: int = 1 << 3  # 1000
    DOWN: int = 1 << 2  # 0100
    LEFT: int = 1 << 1  # 0010
    RIGHT: int = 1  # 0001
    NONE: int = 0  # 0000
