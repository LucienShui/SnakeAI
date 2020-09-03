from __future__ import absolute_import, print_function

import random
import typing

import numpy
from tensorflow import keras


class AbstractDeepQNetwork:

    def __init__(self,
                 observation_shape: tuple,
                 action_dim: int,
                 gamma: float = .9,
                 initial_epsilon: float = 0.1,
                 epsilon_decay: float = 1e-6,
                 final_epsilon: float = 0.02,
                 learning_rate: float = 5e-4):

        self.observation_shape: tuple = observation_shape
        self.action_dim: int = action_dim
        self.gamma: float = gamma
        self.initial_epsilon: float = initial_epsilon
        self.epsilon_decay: float = epsilon_decay
        self.final_epsilon: float = final_epsilon
        self.learning_rate: float = learning_rate

        self.time_step: int = 0
        self.model = self._create_model(self.observation_shape, self.action_dim, self.learning_rate)

    def _create_model(self, input_shape: tuple, output_dim: int, learning_rate: float) -> keras.Model:
        raise NotImplementedError

    def _observation_list_preprocessor(self, observation_list: numpy.ndarray) -> numpy.array:
        raise NotImplementedError

    def _train(self, input_data: numpy.ndarray, label: numpy.ndarray) -> None:
        raise NotImplementedError

    def _remember(self, observation: list,
                  reward: float,
                  done: bool,
                  action: int,
                  next_observation: list) -> None:
        raise NotImplementedError

    def _sample(self) -> typing.Tuple[numpy.array, numpy.array, numpy.array, numpy.array, numpy.array]:
        raise NotImplementedError

    def _need_training(self) -> bool:
        raise NotImplementedError

    @property
    def epsilon(self) -> float:
        return max(self.final_epsilon, self.initial_epsilon - self.time_step * self.epsilon_decay)

    def greedy_action(self, observation: list) -> int:

        if random.random() < self.epsilon:
            return random.randint(1, self.action_dim) - 1
        else:
            return self.action(observation)

    def action(self, observation: list) -> int:
        observation_input: numpy.ndarray = numpy.array([observation])
        prediction: numpy.ndarray = self.model.predict(self._observation_list_preprocessor(observation_input))
        return numpy.argmax(prediction, axis=1)[0]

    def fit(self, observation: list,
            reward: float,
            done: bool,
            action: int,
            next_observation: list) -> None:
        self._remember(observation, reward, done, action, next_observation)

        if self._need_training():
            self.time_step += 1
            self._train(*self._preprocess(*self._sample()))

    def _preprocess(self, observation_list, reward_list, done_list,
                    action_list, next_observation_list) -> (numpy.array, numpy.array):
        """
        get input and label
        :param observation_list: observation list
        :param reward_list: reward list
        :param done_list: donw list
        :param action_list: action list
        :param next_observation_list: next observation list
        :return: input and label
        """
        q_value: numpy.ndarray = self.model.predict(self._observation_list_preprocessor(next_observation_list))

        for i, reward in enumerate(reward_list):
            if done_list[i]:
                q_value[i][action_list[i]] = reward
            else:
                q_value[i][action_list[i]] = reward + self.gamma * numpy.max(q_value[i])

        return self._observation_list_preprocessor(observation_list), q_value

    def save(self, *args, **kwargs):
        self.model.save(*args, **kwargs)

    def load_model(self, *args, **kwargs):
        self.model = keras.models.load_model(*args, **kwargs)
