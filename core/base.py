from __future__ import absolute_import, print_function

import copy


class Action(object):
    UP: int = 1 << 3  # 1000
    DOWN: int = 1 << 2  # 0100
    LEFT: int = 1 << 1  # 0010
    RIGHT: int = 1  # 0001
    NONE: int = 0  # 0000


class Point(object):
    class Type(object):
        NONE: int = 1
        BODY: int = 2
        HEAD: int = 3
        TAIL: int = 4
        APPLE: int = 5
        DIRECT: int = 10086

    def __init__(self, x, y, _type: int = Type.BODY):
        self.x: int = x
        self.y: int = y
        self.type: int = _type

    def __add__(self, other):
        result = copy.deepcopy(other)
        result.x += self.x
        result.y += self.y
        result.type = self.type
        return result

    def __str__(self):
        return '{}, {}'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
