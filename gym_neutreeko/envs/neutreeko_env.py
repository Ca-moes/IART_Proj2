from typing import Tuple

import gym
from gym import error, spaces, utils, logger
from gym.utils import seeding

import numpy as np

from gym_neutreeko.game.engine.gamelogic import NeutreekoGame


class NeutreekoEnv(gym.Env):
    """
    TODO Mudar o que está abaixo. Retirado daqui: https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
    Description:
       In a 5x5 board there are 3 white pieces and 3 black pieces in a specific formation
       The black pieces start first and can move in any direction, they can move until
       they collide with another piece or the edge of the board
       The game ends when the 3 pieces make a line in any direction
    Source:
       This environment corresponds to the Neutreeko game
       Specified here: https://www.neutreeko.net/neutreeko.htm
    Observation:
       Type: Box(0, 2, (5, 5), int8)

        [[0, 1, 0, 1, 0],
         [0, 0, 2, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 2, 0, 2, 0]]

       Num     Observation               Min                     Max
       5,5     Board                     0                       2
    Actions:
        TODO Ainda não tenho a certeza como ficarão as ações
       Type: Discrete(2)
       Num   Action
       0     Push cart to the left
       1     Push cart to the right
       Note: The amount the velocity that is reduced or increased is not
       fixed; it depends on the angle the pole is pointing. This is because
       the center of gravity of the pole increases the amount of energy needed
       to move the cart underneath it
    Reward:
        TODO Rewards ainda vão ser definidas
       Reward is 1 for every step taken, including the termination step
    Starting State:
        The initial board on the Observation details
    Episode Termination:
       One of the players is the winner
       The same board position happened 3 times
       Episode length is greater than 200.
    Solved Requirements:
        TODO
       Considered solved when the average return is greater than or equal to
       195.0 over 100 consecutive trials.
   """
    metadata = {
        'render.modes': ['terminal']
    }

    def __init__(self, render_mode='terminal', max_turns=200):
        super(NeutreekoEnv, self).__init__()

        # Every environment comes with an action_space and an observation_space.
        # These attributes are of type Space
        self.action_space = gym.spaces.Box(0, 60, shape=(2,), dtype=np.uint8) #TODO Isto À esquerda
        self.observation_space = gym.spaces.Box(low=np.int8(0), high=np.int8(2), shape=(5,5), dtype=np.int8)

        self.render_mode = render_mode
        self.max_turns = max_turns

        self.game = NeutreekoGame()
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
            'player': self.game.current_player,
            'player_name': ['white', 'black'][self.game.current_player - 1]
        }

        assert not self.done
        # if self.done:
        #     logger.warn("You are calling 'step()' even though this environment has already returned done = True."
        #                 "You should always call 'reset()' once you receive 'done = True'"
        #                 "-- any further steps are undefined behavior.")
        pos, dir = action
        move_check = self.game.action_handler(pos, dir)

        if move_check:
            move_dir, new_pos = move_check
            reward = 1 # TODO fazer as atualizações direitas
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
