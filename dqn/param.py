from __future__ import absolute_import, print_function


class Param(object):
    GAMMA: float = .9
    QUEUE_SIZE: int = 1 << 10
    BATCH_SIZE: int = 32

    INITIAL_EPSILON: float = .5
    EPSILON_DECAY: float = 1e-3
    LOWER_EPSILON: float = 0

    LEARNING_RATE: float = 1e-4
