from __future__ import absolute_import, print_function

import numpy
from tensorflow import keras

from .naive_dqn import NaiveDeepQNetwork


class DoubleDeepQNetwork(NaiveDeepQNetwork):

    def __init__(self, observation_shape: tuple, action_dim: int,
                 replace_target_q_frequency: int = 10, *args, **kwargs):
        super().__init__(observation_shape, action_dim, *args, **kwargs)
        self.replace_target_q_frequency: int = replace_target_q_frequency
        self.target_model: keras = self._create_model(self.observation_shape, self.action_dim, self.learning_rate)
        self.target_model.set_weights(self.model.get_weights())

    def _preprocess(self, observation_list, reward_list, done_list,
                    action_list, next_observation_list) -> (numpy.array, numpy.array):
        q_value: numpy.ndarray = self.model.predict(self._observation_list_preprocessor(next_observation_list))
        max_idx: numpy.ndarray = numpy.argmax(q_value, axis=1)
        target_q_value: numpy.ndarray = self.target_model.predict(
            self._observation_list_preprocessor(next_observation_list))

        for i, reward in enumerate(reward_list):
            if done_list[i]:
                q_value[i][action_list[i]] = reward
            else:
                q_value[i][action_list[i]] = reward + self.gamma * target_q_value[i][max_idx[i]]

        return self._observation_list_preprocessor(observation_list), q_value

    def _train(self, input_data: numpy.ndarray, label: numpy.ndarray) -> None:
        self.model.fit(input_data, label, verbose=0)

        if self.time_step % self.replace_target_q_frequency == 0:
            self.target_model.set_weights(self.model.get_weights())
