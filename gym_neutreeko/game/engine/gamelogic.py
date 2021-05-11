# Lógica do Jogo: https://github.com/towzeur/gym-abalone/blob/master/gym_abalone/game/engine/gamelogic.py
import numpy as np
from typing import Tuple


class NeutreekoGame:
    # Actions
    UP = (-1, 0)
    DOWN = (+1, 0)
    LEFT = (0, -1)
    RIGHT = (0, +1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, +1)
    DOWN_LEFT = (+1, -1)
    DOWN_RIGHT = (+1, +1)

    # ACTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

    ACTIONS = {'UP': (-1, 0),
               'DOWN': (+1, 0),
               'LEFT': (0, -1),
               'RIGHT': (0, +1),
               'UP_LEFT': (-1, -1),
               'UP_RIGHT': (-1, +1),
               'DOWN_LEFT': (+1, -1),
               'DOWN_RIGHT': (+1, +1)
               }

    # Players
    BLACK = 2
    WHITE = 1

    BOARD_SIZE = 5

    def __init__(self):
        self.board = None
        self.current_player = None

    def reset(self):
        self.board = self.new_board()
        self.current_player = self.BLACK

    @staticmethod
    def new_board():
        """
        returns a fresh starting board
        :return: numpy.array
        """

        return np.array([[0, 1, 0, 1, 0],
                         [0, 0, 2, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 2, 0, 2, 0]])

    def free_cell(self, coords: Tuple[int, int]) -> bool:
        if (coords[0] < 0) | (coords[0] >= self.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= self.BOARD_SIZE):
            return False
        value = self.board[coords[0]][coords[1]]
        return value == 0

    def available_directions(self, coords: Tuple[int, int]):
        dirs = []
        for action_name, action_coords  in self.ACTIONS.items():
            # apply action until it reaches EOB (end of board) or another piece
            attempt_coords = tuple(np.add(coords, action_coords))
            free_cell = self.free_cell(attempt_coords)
            if not free_cell:
                continue
            while free_cell:
                new_coords = attempt_coords
                attempt_coords = tuple(np.add(new_coords, action_coords))
                free_cell = self.free_cell(attempt_coords)

            dirs.append((action_name, new_coords))
        return dirs

    def get_possible_moves(self, player: int):
        # Encontra peças do player
        result = np.where(self.board == player)
        listOfCoordinates = list(zip(result[0], result[1]))
        # Vê quais as direções válidas para essa peça (função à parte para fazer)
        possible_moves = []
        for coords in listOfCoordinates:
            dirs = self.available_directions(coords)
            possible_moves.append((coords, dirs))
        return possible_moves
