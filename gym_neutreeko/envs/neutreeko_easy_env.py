from typing import Tuple

import gym
from gym import error, spaces, utils, logger
from gym.utils import seeding

import numpy as np

from gym_neutreeko.game.engine.gamelogic import NeutreekoEasyGame


class Reward:
    @staticmethod
    def get(move_type):
        return {
            "win": 20,  # winning move
            # "2_row": 5,  # places 2 pieces together
            # "between": 2,  # gets in between 2 opponent pieces
            "default": -1  # makes a move (negative to not enforce unnecessary moves)
        }.get(move_type, -1)


class NeutreekoEasyEnv(gym.Env):
    """
    Description:
       In a 5x5 board there are 3 black pieces in a random formation
       The black pieces can move in any direction, they can move until
       they collide with another piece or the edge of the board
       The game ends when the 3 pieces make a line in any direction
    Source:
       This environment corresponds to a simplified version of the Neutreeko game
       Specified here: https://www.neutreeko.net/neutreeko.htm
    Observation:
       Type: Discrete(2300)

        [[0, 1, 0, 1, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0]]

       All possible board combinations
    Actions:
       Type: Discrete(12)

       Num   Action
       0      0-UP
       1      0-DOWN
       2      0-LEFT
       3      0-RIGHT
       4      1-UP
       5      1-DOWN
       6      1-LEFT
       7      1-RIGHT
       8      2-UP
       9      2-DOWN
       10     2-LEFT
       11     2-RIGHT

          UP   DOWN  LEFT  RIGHT
       0  0     1     2     3
       1  4     5     6     7
       2  8     9     10    11

       The piece 0 is the one with the lowest index. For a piece in coords (x, y), its index is 5*x + y.
    Reward:
       Reward class
    Starting State:
        A randomly generated board
    Episode Termination:
       The player makes 3 in a row
       Episode length is greater than 200.
   """
    metadata = {
        'render.modes': ['terminal']
    }

    def __init__(self, render_mode='terminal', max_turns=200):
        super(NeutreekoEasyEnv, self).__init__()

        # 3 pieces and 4 directions possible
        self.action_space = gym.spaces.Discrete(3*4)
        self.observation_space = gym.spaces.Discrete(2300)

        self.render_mode = render_mode
        self.max_turns = max_turns

        self.game = NeutreekoEasyGame()
        pass

    def step(self, action: int) -> Tuple[object, float, bool, dict]:
        """
        Performs an action on the game and returns info
        :param action:
        :return: observation, reward, done, info
        """
        reward = 0
        info = {
            'old_state': np.copy(self.game.board),
            'turn': self.game.turns_count,
            'action': action,
            'direction': None,
        }

        assert not self.done
        # if self.done:
        #     logger.warn("You are calling 'step()' even though this environment has already returned done = True."
        #                 "You should always call 'reset()' once you receive 'done = True'"
        #                 "-- any further steps are undefined behavior.")
        pos, dir = self.process(action)
        move_check = self.game.action_handler(pos, dir)
        if move_check:
            move_dir, new_pos, move_type = move_check
            reward = Reward.get(move_type)
            info['direction'] = move_dir
            info['new_position'] = new_pos

        return self.observation, reward, self.done, info

    def reset(self) -> None:
        """
        Resets the game
        """
        self.game.reset()

    def render(self, mode='terminal') -> None:
        """
        Renders the game according to the mode
        :param mode: terminal or GUI
        :return:
        """
        if mode == 'terminal':
            self.game.render()

    def close(self):
        """
        Closes the environment and terminates anything if necessary
        """
        pass

    @property
    def done(self) -> bool:
        """
        Checks if the game is done or the max turns were reached
        :return: True if the game is done, false otherwise
        """
        game_over = self.game.game_over
        too_many_turns = (self.game.turns_count > self.max_turns)
        return game_over or too_many_turns

    @property
    def observation(self) -> np.array:
        """
        Returns the game board
        :return: The board as a numpy array
        """
        return np.copy(self.game.board)

    def process(self, action: int) -> Tuple[tuple, str]:
        """
        Convert a action into a position and direction
        :param action: A integer between 0 and 11 representing an action
        :return: A tuple with a position (tuple) and a direction
        """
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        result = np.where(self.game.board == 1)
        list_of_coordinates = list(zip(result[0], result[1]))
        return list_of_coordinates[action // 4], directions[action % 4]
