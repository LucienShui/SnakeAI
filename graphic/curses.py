import curses
import time
import typing

from core import Snake


class CursesSubWindow(object):

    def __init__(self, screen, n_lines, n_cols, begin_y=0, begin_x=0):
        self.screen = screen
        self.n_lines = n_lines
        self.n_cols = n_cols
        self.begin_y = begin_y
        self.begin_x = begin_x

    def add_str(self, y: int, x: int, string: str):
        if y >= self.n_lines:
            raise AssertionError('y = {} is bigger than n_line = {}'.format(y, self.n_lines))

        if len(string) > self.n_cols:
            raise AssertionError('len(str) = {} is bigger than n_cols = {}'.format(len(string), self.n_cols))

        self.screen.addstr(self.begin_y + y, self.begin_x + x, string)

    def refresh(self, *args, **kwargs):
        self.screen.refresh(*args, **kwargs)


class CursesSnake(object):
    key2direction: typing.Dict[int, int] = {
        curses.KEY_UP: Snake.action_space.UP,
        curses.KEY_DOWN: Snake.action_space.DOWN,
        curses.KEY_LEFT: Snake.action_space.LEFT,
        curses.KEY_RIGHT: Snake.action_space.RIGHT
    }

    type2str: typing.Dict[int, str] = {
        Snake.point_type_space.NONE: ' ',
        Snake.point_type_space.HEAD: 'O',
        Snake.point_type_space.BODY: '*',
        Snake.point_type_space.TAIL: 'o',
        Snake.point_type_space.APPLE: '@'
    }

    def __init__(self,
                 shape: typing.Tuple[int, int] = (4, 4),
                 initial_frequency: float = 500,
                 frequency_decay: float = .9,
                 display_info: bool = True):
        """
        create snake with curses
        :param shape: games shape
        :param initial_frequency: the frequency of flushing screen, only required when playing manually
        :param frequency_decay: decay of frequency, only required when playing manually
        :param display_info: display game level and snake's length on the right conner or not
        """
        self.shape = shape
        self.initial_frequency: float = initial_frequency
        self.frequency_decay: float = frequency_decay
        self.display_info: bool = display_info

        self.snake: Snake = Snake(self.shape)

        # the score required by next level
        self.required_score: int = 4
        self.level: int = 1

        # initial curses
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.screen.refresh()
        self.screen.timeout(0)

        # draw bound
        self.__draw_bound(self.screen)

        # game screen
        self.game_screen: CursesSubWindow = CursesSubWindow(self.screen, self.shape[0], self.shape[1] * 2 - 1, 1, 1)

        # info screen
        if self.display_info:
            self.info_screen: CursesSubWindow = CursesSubWindow(self.screen, 4, len('length'), 1, self.shape[1] * 2 + 1)
            self.info_screen.add_str(0, 0, 'level')
            self.info_screen.add_str(2, 0, 'length')

    def __del__(self):
        self.close()

    @property
    def frequency(self) -> float:
        return self.initial_frequency * (self.frequency_decay ** self.level)

    def close(self):
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def __draw_bound(self, screen):
        upper_bar = '⎽' * (self.shape[1] * 2 - 1)
        lower_bar = '⎺' * (self.shape[1] * 2 - 1)

        # chinese char
        col_char = '│'

        screen.addstr(0, 0, ' ' + upper_bar + ' ')
        screen.addstr(self.shape[0] + 1, 0, ' ' + lower_bar + ' ')

        for i in range(self.shape[0]):
            screen.addstr(i + 1, 0, col_char + ' ' * (self.shape[1] * 2 - 1) + col_char)

    def __level_up(self):
        self.level += 1
        self.required_score <<= 1

    def __update_info(self, length, level):
        self.info_screen.add_str(1, 0, str(level))
        self.info_screen.add_str(3, 0, str(length))

    def render(self):
        if self.display_info:
            self.__update_info(self.snake.length, self.level)

        for idx, row in enumerate(self.snake.game_board.data):
            self.game_screen.add_str(idx, 0, ' '.join([self.type2str[each] for each in row]))

        # Render field
        self.screen.refresh()

    def run(self):

        while True:
            # Get last pressed key
            key = self.screen.getch()

            board, reward, done, info = self.step(self.key2direction.get(key, Snake.action_space.NONE))

            if self.snake.length == self.required_score:
                self.__level_up()

            self.render()

            if done:
                break

            time.sleep(self.frequency / 1000)
