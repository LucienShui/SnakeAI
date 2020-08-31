from __future__ import absolute_import, print_function
import numpy
import random
import typing


class ReplayBuffer(object):
    def __init__(self, size):
        self._data = []
        self._capacity = size
        self._next_idx = 0

    def __len__(self):
        return len(self._data)

    def add(self, observation, reward, done, action, next_observation):
        data = (observation, reward, done, action, next_observation)

        if self._next_idx >= len(self._data):
            self._data.append(data)
        else:
            self._data[self._next_idx] = data
        self._next_idx = (self._next_idx + 1) % self._capacity

    def _encode_sample(self, idxes) -> typing.Tuple[numpy.array, numpy.array, numpy.array, numpy.array, numpy.array]:
        """
        :param idxes: index list
        :return: observation_list, reward_list, done_list, action_list, next_observation_list
        """
        observation_list, reward_list, done_list, action_list, next_observation_list = [], [], [], [], []
        for i in idxes:
            observation, reward, done, action, next_observation = self._data[i]
            observation_list.append(numpy.array(observation, copy=False))
            action_list.append(action)
            reward_list.append(reward)
            next_observation_list.append(numpy.array(next_observation, copy=False))
            done_list.append(done)
        return (
            numpy.array(observation_list), numpy.array(reward_list), numpy.array(done_list),
            numpy.array(action_list), numpy.array(next_observation_list)
        )

    def sample(self, sample_size) -> typing.Tuple[numpy.array, numpy.array, numpy.array, numpy.array, numpy.array]:
        """
        :param sample_size: sample size
        :returns numpy.array: observation_list, reward_list, done_list, action_list, next_observation_list
        """
        idxes = [random.randint(0, len(self._data) - 1) for _ in range(sample_size)]
        return self._encode_sample(idxes)

    def clear(self):
        self._data = []
