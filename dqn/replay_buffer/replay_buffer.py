from __future__ import absolute_import, print_function
import numpy as np
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

    def _encode_sample(self, idxes) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        :param idxes: index list
        :return: observation_list, reward_list, done_list, action_list, next_observation_list
        """
        observation_list, reward_list, done_list, action_list, next_observation_list = [], [], [], [], []
        for i in idxes:
            observation, reward, done, action, next_observation = self._data[i]
            observation_list.append(np.array(observation, copy=False))
            action_list.append(action)
            reward_list.append(reward)
            next_observation_list.append(np.array(next_observation, copy=False))
            done_list.append(done)
        return (
            np.array(observation_list), np.array(reward_list), np.array(done_list),
            np.array(action_list), np.array(next_observation_list)
        )

    def sample(self, batch_size) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        :param batch_size: batch size
        :returns numpy.array: observation_list, reward_list, done_list, action_list, next_observation_list
        """
        idxes = [random.randint(0, len(self._data) - 1) for _ in range(batch_size)]
        return self._encode_sample(idxes)
