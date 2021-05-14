# Onde vai ocorrer o jogo e haver a interação Agente-Ambiente
# https://github.com/towzeur/gym-abalone/blob/master/examples/demo.py
import numpy as np
from gym_neutreeko.game.common.gameutils import NeutreekoUtils as utils

if __name__ == "__main__":

    board = np.array([[0, 1, 2, 3, 4],
                      [5, 6, 7, 8, 9],
                      [8, 7, 6, 5, 4],
                      [3, 2, 1, 0, 1],
                      [2, 3, 4, 5, 6]], dtype=np.int8)
    print(f'type board -> {type(board)}')

    for i in range(5):
        print(f'type line -> {type(board[i, :])}')
        print(utils.search_sequence_numpy(board[i, :], np.array([1, 1, 1])))
    print()
    for i in range(5):
        print(board[:, i])
    print()

    print(np.diagonal(board, offset=-2))
    print(np.diagonal(board, offset=-1))
    print(np.diagonal(board))
    print(np.diagonal(board, offset=1))
    print(np.diagonal(board, offset=2))

    print()
    flipped_board = np.fliplr(board)
    print(flipped_board, '\n')
    print(np.diagonal(flipped_board, offset=-2))
    print(np.diagonal(flipped_board, offset=-1))
    print(np.diagonal(flipped_board))
    print(np.diagonal(flipped_board, offset=1))
    print(np.diagonal(flipped_board, offset=2))

