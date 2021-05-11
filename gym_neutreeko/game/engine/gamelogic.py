# Lógica do Jogo: https://github.com/towzeur/gym-abalone/blob/master/gym_abalone/game/engine/gamelogic.py
import numpy
import numpy as np


class NeutreekoGame:
    # PLAYERS
    BLACK = 2
    WHITE = 1

    def __init__(self):
        self.board = None
        self.turn = None

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

    def get_possible_moves(self, player: int):
        pass
        # Encontra peças do player (a fazer em main)

        # Vê quais as direções válidas para essa peça (função à parte para fazer)

        # retorna isso
