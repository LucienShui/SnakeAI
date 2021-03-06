from __future__ import absolute_import, print_function

import typing

import numpy
from tensorflow import keras

from core import Point
from .naive_dqn import NaiveDeepQNetwork


class CNNDeepQNetwork(NaiveDeepQNetwork):

    def __init__(self, observation_shape: tuple, action_dim: int, *args, **kwargs):
        super().__init__(observation_shape, action_dim, *args, **kwargs)

    def _observation_list_preprocessor(self, observation_list: numpy.ndarray) -> numpy.array:
        shape: list = list(observation_list.shape) + [1]
        return observation_list.reshape(shape) / Point.Type.MAX

    @classmethod
    def _create_model(cls, input_shape: typing.Tuple[int, int], output_dim: int,
                      learning_rate: float = 1e-4) -> keras.Model:
        model: keras.Model = keras.models.Sequential([
            keras.layers.Conv2D(8, (3, 3), activation=keras.activations.relu,
                                input_shape=(input_shape[0], input_shape[1], 1)),
            keras.layers.MaxPooling2D(2, 2),

            keras.layers.Dropout(.5),
            keras.layers.Flatten(),

            keras.layers.Dense(64, activation=keras.activations.relu),
            keras.layers.Dense(32, activation=keras.activations.relu),
            keras.layers.Dense(output_dim, activation=keras.activations.linear),
        ])

        model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                      loss=keras.losses.mean_squared_error,
                      metrics=[keras.losses.mean_squared_error])

        return model
