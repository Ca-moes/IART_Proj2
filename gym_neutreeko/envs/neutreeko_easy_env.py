from typing import Tuple

import gym
from gym import error, spaces, utils, logger
from gym.utils import seeding
from gym_neutreeko.game.common.gameutils import Reward

import numpy as np

from gym_neutreeko.game.engine.gamelogic import NeutreekoEasyGame


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
       Type: Box(0, 2, (5, 5), int8)

        [[0, 1, 0, 3, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 2, 0, 0],
         [0, 0, 0, 0, 0]]

       Num     Observation               Min                     Max
       5,5     Board                     0                       2
    Actions:
       Type: Discrete(4)
       Num   Action
       0      1-UP
       1      1-DOWN
       2      1-LEFT
       3      1-RIGHT
       4      2-UP
       5      2-DOWN
       6      2-LEFT
       7      2-RIGHT
       8      3-UP
       9      3-DOWN
       10     3-LEFT
       11     3-RIGHT

       The piece 1 is the one with the lowest index. For a piece in coords (x, y), its index is 5*x + y.
    Reward:
       Reward is 10 for the end step and -0.1 for each other step
    Starting State:
        The initial board is a not out of the gate random winning board
    Episode Termination:
       The player makes 3 in a row
       Episode length is greater than 200.
    Solved Requirements:
        TODO Dunno
       Considered solved when the average return is greater than or equal to
       195.0 over 100 consecutive trials.
   """
    metadata = {
        'render.modes': ['terminal']
    }

    def __init__(self, render_mode='terminal', max_turns=200):
        super(NeutreekoEasyEnv, self).__init__()

        # 3 pieces and 8 directions possible
        self.action_space = gym.spaces.Discrete(4*3)
        self.observation_space = gym.spaces.Box(low=np.int8(0), high=np.int8(2), shape=(5, 5), dtype=np.int8)

        self.render_mode = render_mode
        self.max_turns = max_turns

        self.game = NeutreekoEasyGame()
        pass

    def step(self, action) -> Tuple[object, float, bool, dict]:
        """
        implementation of the classic “agent-environment loop”.

        Args:
           action (object) : the board
        Returns:
           observation (object):
           reward (float)
           done (boolean)
           info (dict)

        :param action:
        :return:
        """

        reward = 0
        info = {
            'turn': self.game.turns_count,
            'direction': None,
        }

        assert not self.done
        # if self.done:
        #     logger.warn("You are calling 'step()' even though this environment has already returned done = True."
        #                 "You should always call 'reset()' once you receive 'done = True'"
        #                 "-- any further steps are undefined behavior.")
        pos, dir = action
        move_check = self.game.action_handler(pos, dir)

        if move_check:
            move_dir, new_pos, move_type = move_check
            reward = Reward.method_1(move_type)
            info['direction'] = move_dir
            info['new_position'] = new_pos

        return self.observation, reward, self.done, info

    def reset(self):
        self.game.reset()
        pass

    def render(self, mode='terminal'):
        if mode == 'terminal':
            self.game.render()
        pass

    def close(self):
        pass

    @property
    def done(self):
        game_over = self.game.game_over
        too_many_turns = (self.game.turns_count > self.max_turns)
        return game_over or too_many_turns

    @property
    def observation(self):
        return np.copy(self.game.board)
