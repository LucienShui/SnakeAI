from __future__ import absolute_import, print_function

import math
from agent import DeepQLearningNetwork
from graphic import CursesSnake
from gym.envs import SnakeEnv

# TRAINING: bool = True
TRAINING: bool = False
RENDER: bool = True
SHAPE: tuple = (9, 9)


def custom_reward(info: dict) -> float:
    snake_x = info['bodies'][0]['x']
    snake_y = info['bodies'][0]['y']

    apple_x = info['apple']['x']
    apple_y = info['apple']['y']

    return 1 / math.sqrt(math.pow(snake_x - apple_x, 2) + math.pow(snake_y - apple_y, 2))


def main():
    env = SnakeEnv(SHAPE)

    dqn = DeepQLearningNetwork(SHAPE,
                               len(env.action_space),
                               initial_epsilon=.5,
                               batch_size=64,
                               queue_size=1 << 8)

    if not TRAINING:
        dqn.load_model('model.h5')

    best_score: int = 0

    for i_episode in range(2000):
        observation = env.reset()
        for t in range(1000):
            if RENDER:
                env.render()
            action = dqn.greedy_action(observation) if TRAINING else dqn.action(observation)
            next_observation, reward, done, info = env.step(action)

            if TRAINING:
                dqn.fit(observation, reward, done, action, next_observation)

            observation = next_observation
            if done:
                best_score = max(best_score, t + 1)
                if (i_episode + 1) % 100 == 0:
                    dqn.save('model.h5')
                    print("Episode {} finished after {} time steps, best score is {}, dqn.epsilon = {}".format(
                        i_episode + 1, t + 1, best_score, dqn.epsilon))
                break
    env.close()

    if TRAINING:
        dqn.save('model.h5')


def human():
    CursesSnake(SHAPE).run()


if __name__ == '__main__':
    # human()
    main()
