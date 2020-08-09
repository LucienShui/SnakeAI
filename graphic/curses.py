import curses
import time
import typing

from core import Snake


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

    def __init__(self, width: int = 9, height: int = 9, frequency: int = 200):
        self.width: int = width
        self.height: int = height
        self.frequency: int = frequency

        self.next_level: int = 4

    def draw_bound(self, screen, raw_offset: int):
        upper_bar = '⎽' * (self.width * 2 - 1)
        lower_bar = '⎺' * (self.width * 2 - 1)
        col_char = '│'

        screen.addstr(0, 0, 'length: {}'.format(0))
        screen.addstr(1, 0, ' ' + upper_bar + ' ')
        screen.addstr(self.height + raw_offset, 0, ' ' + lower_bar + ' ')

        for i in range(self.height):
            screen.addstr(i + raw_offset, 0, col_char + upper_bar + col_char)

    @classmethod
    def update_length(cls, screen, length: int):
        screen.addstr(0, 0, 'length: {}'.format(length))

    def main(self, screen):

        screen.timeout(0)

        raw_offset = 2

        self.draw_bound(screen, raw_offset)

        snake: Snake = Snake(self.width, self.height)

        while True:
            # Get last pressed key
            key = screen.getch()

            board, reward, done, info = snake.step(self.key2direction.get(key, Snake.action_space.NONE))

            if done:
                break

            self.update_length(screen, snake.length)

            if snake.length == self.next_level:
                self.next_level <<= 1
                self.frequency *= .8

            for idx, row in enumerate(board):
                screen.addstr(idx + raw_offset, 1, ' '.join([self.type2str[each] for each in row]))

            # Render field
            screen.refresh()

            time.sleep(self.frequency / 1000)

    def run(self):
        curses.wrapper(self.main)
