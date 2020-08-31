from __future__ import absolute_import, print_function

import random
import typing
from dqn.replay_buffer import ReplayBuffer

import numpy
from tensorflow import keras


class AbstractDeepQNetwork(object):

    def __init__(self,
                 observation_shape: tuple,
                 action_dim: int,
                 gamma: float = .9,
                 queue_size: int = 1 << 16,
                 batch_size: int = 32,
                 initial_epsilon: float = 0.1,
                 epsilon_decay: float = 1e-6,
                 final_epsilon: float = 0.02,
                 learning_rate: float = 5e-4):

        self.observation_shape: tuple = observation_shape
        self.action_dim: int = action_dim
        self.gamma: float = gamma
        self.queue_size: int = queue_size
        self.batch_size: int = batch_size
        self.initial_epsilon: float = initial_epsilon
        self.epsilon_decay: float = epsilon_decay
        self.final_epsilon: float = final_epsilon
        self.learning_rate: float = learning_rate

        self.time_step: int = 0
        self.replay_buffer: ReplayBuffer = ReplayBuffer(self.queue_size)
        self.model = self.init_model(self.observation_shape, self.action_dim, self.learning_rate)

    @classmethod
    def init_model(cls, input_shape: tuple, output_dim: int, learning_rate: float) -> keras.Model:
        raise NotImplementedError

    @property
    def epsilon(self) -> float:
        return max(self.final_epsilon, self.initial_epsilon - self.time_step * self.epsilon_decay)

    def greedy_action(self, observation: list) -> int:

        if random.random() < self.epsilon:
            return random.randint(1, self.action_dim) - 1
        else:
            return self.action(observation)

    def observation_list_preprocessor(self, observation_list: numpy.ndarray) -> numpy.ndarray:
        raise NotImplementedError

    def action(self, observation: list) -> int:
        observation_input: numpy.ndarray = numpy.array([observation])
        prediction: numpy.ndarray = self.model.predict(self.observation_list_preprocessor(observation_input))
        return numpy.argmax(prediction, axis=1)[0]

    def fit(self, observation: list,
            reward: float,
            done: bool,
            action: int,
            next_observation: list) -> None:
        self.replay_buffer.add(observation, reward, done, action, next_observation)

        if len(self.replay_buffer) >= self.batch_size:
            self.__fit(*self.replay_buffer.sample(self.batch_size))

    def __fit(self, observation_list, reward_list, done_list, action_list, next_observation_list):
        self.time_step += 1

        q_value: numpy.ndarray = self.model.predict(self.observation_list_preprocessor(next_observation_list))

        for i, reward in enumerate(reward_list):
            if done_list[i]:
                q_value[i][action_list[i]] = reward
            else:
                idx = numpy.argmax(q_value[i])
                q_value[i][idx] = reward + self.gamma * q_value[i][idx]

        self.model.fit(self.observation_list_preprocessor(observation_list), q_value, verbose=0)

    def save(self, *args, **kwargs):
        self.model.save(*args, **kwargs)

    def load_model(self, *args, **kwargs):
        self.model = keras.models.load_model(*args, **kwargs)
