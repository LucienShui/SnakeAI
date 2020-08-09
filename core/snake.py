import copy
import typing


class Action(object):
    UP: int = 1 << 3  # 1000
    DOWN: int = 1 << 2  # 0100
    LEFT: int = 1 << 1  # 0010
    RIGHT: int = 1  # 0001
    NONE: int = 0  # 0000

    def __init__(self, action: int):
        self.action: int = action


class Point(object):
    class Type(object):
        NONE: int = 0
        BODY: int = 1
        HEAD: int = 2
        TAIL: int = 3
        APPLE: int = 4
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


class Apple(object):
    def __init__(self, point: Point):
        self.position: Point = point


class Snake(object):

    def __init__(self, x: int, y: int, length: int = 2):
        self.points: typing.List[Point] = [Point(x, y, Point.Type.HEAD)]

        for i in range(1, length - 1):
            self.points.append(Point(x, y - i))

        self.points.append(Point(x, y + length - 1, Point.Type.TAIL))

        self.delta: Point = Point(0, 1, Point.Type.DIRECT)
        self.direction = Action.RIGHT

    def move(self, apple: Apple) -> bool:
        self.points.insert(0, self.points[0] + self.delta)

        self.points[1].type = Point.Type.BODY

        if self.points[0] == apple.position:
            return True

        self.points.pop()
        self.points[-1].type = Point.Type.TAIL
        return False

    def change_direction(self, direction: int) -> None:
        """
        调整蛇头的方向
        :param direction:
        :return:
        """
        if self.direction == direction:
            return
        if self.direction & 12 and direction & 12:
            return
        if self.direction & 3 and direction & 3:
            return

        self.direction = direction

        if direction & 12:
            self.delta.x = 1 if direction == Action.DOWN else -1
            self.delta.y = 0
        else:
            self.delta.x = 0
            self.delta.y = -1 if direction == Action.LEFT else 1

    def __getitem__(self, index: int) -> Point:
        return self.points[index]
