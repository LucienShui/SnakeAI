from __future__ import absolute_import, print_function

import numpy
import typing

from .naive_dqn import NaiveDeepQNetwork


class DeepQNetworkWithDrop(NaiveDeepQNetwork):

    def __init__(self, observation_shape: tuple, action_dim: int, *args, **kwargs):
        super().__init__(observation_shape, action_dim, *args, **kwargs)

    def _need_training(self) -> bool:
        return len(self.replay_buffer) == self.buffer_size

    def _sample(self) -> typing.Tuple[numpy.array, numpy.array, numpy.array, numpy.array, numpy.array]:
        result = self.replay_buffer.sample(self.buffer_size)
        self.replay_buffer.clear()
        return result

    def _train(self, input_data: numpy.array, label: numpy.array) -> None:
        self.model.fit(input_data, label, epochs=10, batch_size=self.batch_size, verbose=0)
