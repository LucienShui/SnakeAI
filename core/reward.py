from __future__ import absolute_import, print_function


class Reward(object):
    # Negative
    DEATH: int = -.1
    NORMAL_ACTION: int = -.01
    SAME_ACTION: int = -.1
    TOO_MANY_ACTION: int = -.1

    # Positive
    APPLE: int = 1
    WIN: int = 1
