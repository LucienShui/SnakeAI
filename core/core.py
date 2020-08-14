import random
import typing

from .snake import Apple, Point, Snake, Action


class GameBoard(object):

    def __init__(self, shape: typing.Tuple[int, int]):
        self.shape = shape
        self.data: typing.List[typing.List[int]] = [[0 for _ in range(self.shape[1])] for _ in range(self.shape[0])]

    def clear(self):
        """
        清除画布
        :return: None
        """
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
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

    def __init__(self, shape: typing.Tuple[int, int], length: int = 2):
        # 初始画布
        self.shape = shape
        self.init_length: int = length
        self.game_board: GameBoard = GameBoard(self.shape)

        # 蛇
        self.snake: Snake = Snake(self.shape[1] >> 1, (self.shape[0] >> 1) - self.init_length + 1, self.init_length)
        self.game_board.draw_points(self.snake.points)

        # 初始化蛇之后才能初始化苹果
        self.apple: Apple = self.get_apple()
        self.game_board.draw_point(self.apple.position)

        self.score = 0

    def __str__(self):
        return '\n'.join([
            '  '.join([
                self.game_board[i][j].__str__() for j in range(self.shape[1])]) for i in range(self.shape[0])])

    @property
    def length(self) -> int:
        return self.init_length + self.score

    def is_out_range(self, point: Point) -> bool:
        """
        判断点是否越界
        :param point: 点
        :return: 是 or 否
        """
        return not (0 <= point.x < self.shape[0] and 0 <= point.y < self.shape[1])

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

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.game_board[i][j] == 0:
                    candidate_point.append(Point(i, j, Point.Type.APPLE))

        return Apple(random.choice(candidate_point))

    def step(self, action: int) -> (typing.List[typing.List[int]], int, bool, typing.Any):
        """
        走一步
        :param action: 执行的动作，详见 self.action_space
        :return:
            observation: typing.List[typing.List[int]] 游戏画布
            reward: int 奖励，如果吃到果子会是 1，反之是 0
            is_crash: bool 游戏是否结束
            info: typing.Any 可以是任何附加信息
        """
        self.game_board.clear()

        if action != Action.NONE:
            self.snake.change_direction(action)
        eat_apple: bool = self.snake.move(self.apple)

        if self.is_crash():
            return self.game_board.data, -0x3f3f3f3f, True, None

        self.game_board.draw_points(self.snake.points)

        if eat_apple:
            self.score += 1

            if self.length == self.shape[1] * self.shape[0]:
                return self.game_board.data, 0x3f3f3f3f, True, None

            self.apple = self.get_apple()

        self.game_board.draw_point(self.apple.position)

        return self.game_board.data, int(eat_apple), False, None
