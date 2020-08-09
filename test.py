import typing
import unittest

from core import Snake


class SnakeTestCase(unittest.TestCase):

    def test_snake(self):
        key2direction: typing.Dict[str, int] = {
            'w': Snake.action_space.UP,
            's': Snake.action_space.DOWN,
            'a': Snake.action_space.LEFT,
            'd': Snake.action_space.RIGHT
        }

        test_case_set: typing.List[typing.Tuple[int, int, str, int]] = [
            (5, 5, '....', 1),
            (5, 5, 'aaaa', 1),
            (5, 5, '...w', 0),
        ]

        for width, height, keys, expected in test_case_set:
            game: Snake = Snake(width, height)
            flag = -1
            for key in keys:
                observation, reward, is_crash, info = game.step(key2direction.get(key, Snake.action_space.NONE))
                flag = 1 if is_crash else 0
            self.assertEqual(expected, flag)


if __name__ == '__main__':
    unittest.main()
