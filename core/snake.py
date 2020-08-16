import typing

from .base import Point, Action


class Apple(object):
    def __init__(self, point: Point):
        self.position: Point = point


class Snake(object):

    def __init__(self, x: int, y: int, length: int = 2):
        self.length: int = length
        self.initial_x: int = x
        self.initial_y: int = y

        self.points: typing.List[Point] = ...
        self.delta: Point = ...
        self.direction: int = ...

        self.reset()

    def reset(self):
        self.points: typing.List[Point] = [Point(self.initial_x, self.initial_y, Point.Type.HEAD)]

        for i in range(1, self.length - 1):
            self.points.append(Point(self.initial_x, self.initial_y - i))

        self.points.append(Point(self.initial_x, self.initial_y + self.length - 1, Point.Type.TAIL))

        self.delta: Point = Point(0, 1, Point.Type.DIRECT)
        self.direction: int = Action.RIGHT

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
