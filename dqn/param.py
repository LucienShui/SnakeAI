from __future__ import absolute_import, print_function


class Param(object):
    GAMMA: float = .9
    QUEUE_SIZE: int = 1 << 16
    BATCH_SIZE: int = 32

    INITIAL_EPSILON: float = .1
    EPSILON_DECAY: float = 1e-5
    FINAL_EPSILON: float = 0.02

    LEARNING_RATE: float = 5e-4

    RESET_AFTER_TRAINING: bool = True
