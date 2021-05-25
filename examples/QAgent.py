import gym
import numpy as np


class QAgent:
    def __init__(self, observation_space=2300, action_space=12):
        """
        Initialize an agent and its parameters

        :param observation_space: How many possible states there are
        :param action_space: How many actions there are
        """
        self.Q = np.zeros((observation_space, action_space))

        self.alpha = 0.7  # learning rate
        self.discount_factor = 0.618
        self.epsilon = 1
        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.decay = 0.001

        self.board_dict = {}
        self.lastID = None

    def choice(self, env) -> int:
        """
        Given the environment, choose the action to take

        :param env: A Game environment
        :return: the action to take
        """
        # Choosing an action given the states based on a random number
        exp_exp_tradeoff = np.random.uniform(0, 1)

        if repr(env.observation) not in self.board_dict:
            if self.lastID:
                self.lastID += 1
            else:
                self.lastID = 0
            self.board_dict[repr(env.observation)] = self.lastID
            state = self.lastID
        else:
            state = self.board_dict[repr(env.observation)]
        # STEP 2: FIRST option for choosing the initial action - exploit
        # If the random number is larger than epsilon: employing exploitation
        # and selecting best action
        if exp_exp_tradeoff > self.epsilon:
            action = np.argmax(self.Q[state, :])
            # Sometimes the agent will try to exploit, but end up choosing a not valid move
            # To ensure that exploiting always provides good results, there's a check to verify if the
            # action is valid, if it is not, chooses a random valid move
            possible_moves = env.game.get_possible_moves(1, only_valid=True)
            if action not in possible_moves:
                i_random = np.random.randint(len(possible_moves))
                action = possible_moves[i_random]

        # STEP 2: SECOND option for choosing the initial action - explore
        # Otherwise, employing exploration: choosing a random action
        else:
            possible_moves = env.game.get_possible_moves(1, only_valid=True)
            i_random = np.random.randint(len(possible_moves))
            action = possible_moves[i_random]

        return action

    def update(self, obs, reward: int, done: bool, info: dict, env) -> None:
        """
        Updates the Q-table after performing an action

        :param obs: New state that resulted from a action
        :param reward: The reward returned from applying a action to a state
        :param done: Boolean representing if the episode is finished
        :param info: Additional info from performing an action
        :param env: The environment
        """
        if repr(obs) not in self.board_dict:
            if not self.board_dict:
                self.board_dict[repr(obs)] = 0
                self.lastID = 0
            else:
                self.lastID += 1
                self.board_dict[repr(obs)] = self.lastID

        state = self.board_dict[repr(info["old_state"])]
        new_state = self.board_dict[repr(obs)]
        action = info['action']

        self.Q[state, action] = self.Q[state, action] + self.alpha * (reward + self.discount_factor * np.max(self.Q[new_state, :]) - self.Q[state, action])

    def episode_update(self, episode: int) -> None:
        """
        Update internals after each episode

        :param episode: Finished episode id
        """
        # Cutting down on exploration by reducing the epsilon
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon)*np.exp(-self.decay*episode)
