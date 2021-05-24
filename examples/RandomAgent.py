import numpy as np


class RandomAgent:
    def __init__(self):
        board_dict = {}

    def choice(self, env):
        player = env.game.current_player
        possible_moves = env.game.get_possible_moves(player, only_valid=True)

        i_random = np.random.randint(len(possible_moves))
        return possible_moves[i_random]

    def update(self, obs, reward, done, info):
        pass
