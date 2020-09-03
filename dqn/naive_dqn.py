from __future__ import absolute_import, print_function

import typing

import numpy
from tensorflow import keras

from .abstract_dqn import AbstractDeepQNetwork
from .replay_buffer import ReplayBuffer


class NaiveDeepQNetwork(AbstractDeepQNetwork):
    def __init__(self, observation_shape: tuple,
                 action_dim: int,
                 batch_size: int = 32,
                 buffer_size: int = 1 << 10,
                 *args, **kwargs):
        super().__init__(observation_shape, action_dim, *args, **kwargs)
        self.buffer_size: int = buffer_size
        self.batch_size: int = batch_size

        self.replay_buffer: ReplayBuffer = ReplayBuffer(self.buffer_size)

    def _create_model(self, input_shape: tuple, output_dim: int, learning_rate: float) -> keras.Model:
        model: keras.Model = keras.models.Sequential([
            keras.layers.Flatten(input_shape=input_shape),

            keras.layers.Dense(64, activation=keras.activations.relu),
            keras.layers.Dense(32, activation=keras.activations.relu),
            keras.layers.Dense(output_dim, activation=keras.activations.linear),
        ])

        model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                      loss=keras.losses.mean_squared_error,
                      metrics=[keras.losses.mean_squared_error])
        return model

    def _observation_list_preprocessor(self, observation_list: numpy.ndarray) -> numpy.array:
        return observation_list

    def _train(self, input_data: numpy.ndarray, label: numpy.ndarray) -> None:
        self.model.fit(input_data, label, verbose=0)

    def _remember(self, observation: list,
                  reward: float,
                  done: bool,
                  action: int,
                  next_observation: list) -> None:
        self.replay_buffer.add(observation, reward, done, action, next_observation)

    def _sample(self) -> typing.Tuple[numpy.array, numpy.array, numpy.array, numpy.array, numpy.array]:
        return self.replay_buffer.sample(self.batch_size)

    def _need_training(self) -> bool:
        return self.buffer_size >= self.batch_size
