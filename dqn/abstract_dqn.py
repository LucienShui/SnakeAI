from __future__ import absolute_import, print_function

import random
import typing
from queue import Queue

import numpy
from tensorflow import keras


class AbstractDeepQNetwork(object):

    def __init__(self,
                 observation_shape: tuple,
                 action_dim: int,
                 gamma: float = .9,
                 queue_size: int = 1 << 10,
                 batch_size: int = 32,
                 initial_epsilon: float = 1,
                 epsilon_decay: float = 1e-4,
                 lower_epsilon: float = 0,
                 learning_rate: float = 1e-4):

        self.observation_shape: tuple = observation_shape
        self.action_dim: int = action_dim
        self.gamma: float = gamma
        self.queue_size: int = queue_size
        self.batch_size: int = batch_size
        self.initial_epsilon: float = initial_epsilon
        self.epsilon_decay: float = epsilon_decay
        self.lower_epsilon: float = lower_epsilon
        self.learning_rate: float = learning_rate

        self.time_step: int = 0
        self.queue: Queue = Queue()
        self.model = self.init_model(self.observation_shape, self.action_dim, self.learning_rate)

    @classmethod
    def init_model(cls, input_shape: tuple, output_dim: int,
                   learning_rate: float = 1e-4) -> keras.Model:
        raise NotImplementedError

    @property
    def epsilon(self) -> float:
        return max(0., self.initial_epsilon - self.time_step * self.epsilon_decay)

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
        self.queue.put((observation, reward, done, action, next_observation))

        if self.queue.qsize() == self.queue_size:
            train_data: list = list(self.queue.queue)
            random.shuffle(train_data)
            self.queue = Queue()  # 清空队列
            self.__fit(train_data)

    def __fit(self, sample: typing.List[typing.Tuple[list, float, bool, int, list]]):
        self.time_step += 1

        observation_list, reward_list, done_list, action_list, new_observation_list = [
            numpy.array([each[i] for each in sample]) for i in range(5)
        ]

        q_value: numpy.ndarray = self.model.predict(self.observation_list_preprocessor(new_observation_list))

        for i, reward in enumerate(reward_list):
            if done_list[i]:
                q_value[i][action_list[i]] = reward
            else:
                idx = numpy.argmax(q_value[i])
                q_value[i][idx] = reward + self.gamma * q_value[i][idx]

        self.model.fit(self.observation_list_preprocessor(observation_list),
                       q_value, batch_size=self.batch_size, epochs=8, verbose=0)

    def save(self, *args, **kwargs):
        self.model.save(*args, **kwargs)

    def load_model(self, *args, **kwargs):
        self.model = keras.models.load_model(*args, **kwargs)
