import gym
import numpy as np


class SARSAAgent:
    def __init__(self, observation_space=2300, action_space=12):
        self.Q = np.zeros((observation_space, action_space))

        self.alpha = 0.7  # learning rate
        self.discount_factor = 0.618
        self.epsilon = 1
        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.decay = 0.005

        self.board_dict = {}
        self.lastID = None

    def choice(self, env):
        # Choosing an action given the states based on a random number
        exp_exp_tradeoff = np.random.uniform(0, 1)

        if repr(env.state()) not in self.board_dict:
            if self.lastID:
                self.lastID += 1
            else:
                self.lastID = 0
            self.board_dict[repr(env.state())] = self.lastID
            state = self.lastID
        else:
            state = self.board_dict[repr(env.state())]
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

    def update(self, obs, reward, done, info):
        if repr(obs) not in self.board_dict:
            if not self.board_dict:
                self.board_dict[repr(obs)] = 0
                self.lastID = 0
            else:
                self.lastID += 1
                self.board_dict[repr(obs)] = self.lastID

        # print(f'dict -> {self.board_dict}')
        # print(f'board -> {repr(info["old_state"])}')
        # print(f'state -> {self.board_dict[repr(info["old_state"])]}')

        state = self.board_dict[repr(info["old_state"])]
        new_state = self.board_dict[repr(obs)]
        action = info['action']

        self.Q[state, action] = self.Q[state, action] + self.alpha * (reward + self.discount_factor * np.max(self.Q[new_state, :]) - self.Q[state, action])

        # TODO atualiza a table com um novo state, mas não o executa

