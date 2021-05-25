import numpy as np


class RandomAgent:
    def __init__(self):
        pass

    def choice(self, env) -> int:
        """
        Given the environment, choose the action to take using randomness
        :param env: A Game environment
        :return: the action to take
        """
        player = env.game.current_player
        possible_moves = env.game.get_possible_moves(player, only_valid=True)
        i_random = np.random.randint(len(possible_moves))
        return possible_moves[i_random]

    def update(self, obs, reward, done, info, env):
        """
        Not used in this agent
        """
        pass

    def episode_update(self, episode):
        """
        Not used in this agent
        """
        pass
