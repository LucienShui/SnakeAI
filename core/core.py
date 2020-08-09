import random
import typing

from .snake import Apple, Point, Snake, Action


class GameBoard(object):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data: typing.List[typing.List[int]] = [[0 for j in range(self.width)] for i in range(self.height)]

    def clear(self):
        """
        清除画布
        :return: None
        """
        for i in range(self.height):
            for j in range(self.width):
                self.data[i][j] = 0

    def draw_points(self, points: typing.List[Point]) -> None:
        """
        画多个点，直接覆盖
        :param points: Point List
        :return: None
        """
        for point in points:
            self.draw_point(point)

    def draw_point(self, point: Point) -> None:
        """
        画一个点，直接覆盖
        :param point: Point List
        :return: None
        """
        self.data[point.x][point.y] = point.type

    def __getitem__(self, index) -> typing.List[int]:
        return self.data[index]


class Game(object):
    action_space: Action = Action
    point_type_space: Point.Type = Point.Type

    def __init__(self, width: int, height: int, length: int = 2):
        # 初始画布
        self.width: int = width
        self.height: int = height
        self.init_length: int = length
        self.game_board: GameBoard = GameBoard(width, height)

        # 蛇
        self.snake: Snake = Snake(self.width >> 1, (self.height >> 1) - self.init_length + 1, self.init_length)
        self.game_board.draw_points(self.snake.points)

        # 初始化蛇之后才能初始化苹果
        self.apple: Apple = self.get_apple()
        self.game_board.draw_point(self.apple.position)

        self.score = 0

    def __str__(self):
        return '\n'.join([
            '  '.join([
                self.game_board[i][j].__str__() for j in range(self.width)]) for i in range(self.height)])

    @property
    def length(self) -> int:
        return self.init_length + self.score

    def is_out_range(self, point: Point) -> bool:
        """
        判断点是否越界
        :param point: 点
        :return: 是 or 否
        """
        return not (0 <= point.x < self.width and 0 <= point.y < self.height)

    def is_crash(self) -> bool:
        """
        :return: 游戏是否结束
        """
        return self.is_out_range(self.snake[0]) or self.snake[0] in self.snake[1:]

    def get_apple(self) -> Apple:
        """
        从画布空白的部分选出一点作为苹果
        :return: 苹果的对象
        """

        candidate_point: typing.List[Point] = []

        for i in range(self.height):
            for j in range(self.width):
                if self.game_board[i][j] == 0:
                    candidate_point.append(Point(i, j, Point.Type.APPLE))

        return Apple(random.choice(candidate_point))

    def step(self, action: int) -> (typing.List[typing.List[int]], bool):
        """
        走一步
        :param action:
        :return:
            game_board: typing.List[typing.List[int]] 游戏画布
            is_crash: bool 游戏是否结束
        """
        self.game_board.clear()

        if action != Action.NONE:
            self.snake.change_direction(action)
        eat_apple: bool = self.snake.move(self.apple)

        if self.is_crash():
            return self.game_board.data, True

        self.game_board.draw_points(self.snake.points)

        if eat_apple:
            self.apple = self.get_apple()
            self.score += 1

        self.game_board.draw_point(self.apple.position)

        return self.game_board.data, False
