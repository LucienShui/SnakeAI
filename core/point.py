from __future__ import absolute_import, print_function

import copy


class Point(object):
    class Type(object):
        NONE: int = 0
        BODY: int = 1
        HEAD: int = 2
        TAIL: int = 3
        APPLE: int = 4
        DIRECT: int = -1
        MAX: int = 4

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
