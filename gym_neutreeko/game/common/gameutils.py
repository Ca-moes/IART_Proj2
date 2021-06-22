from typing import Tuple, Union

import numpy as np

from gym_neutreeko.game.common import const


class NeutreekoUtils:
    @staticmethod
    def search_sequence_numpy(arr, seq) -> bool:
        """
        Find sequence in an array using NumPy only.
        :param arr: input 1D array
        :param seq: input 1D array
        :return: True if the seq is in the arr
        """

        # Store sizes of input array and sequence
        Na, Nseq = arr.size, seq.size

        # Range of sequence
        r_seq = np.arange(Nseq)

        # Create a 2D array of sliding indices across the entire length of input array.
        # Match up with the input sequence & get the matching starting indices.
        M = (arr[np.arange(Na-Nseq+1)[:, None] + r_seq] == seq).all(1)

        # Return true if the sequence exists
        return M.any() > 0

        # Get the range of those indices as final output
        # if M.any() > 0:
        #     return np.where(np.convolve(M, np.ones(Nseq, dtype=int)) > 0)[0]
        # else:
        #     return []         # No match found

    @staticmethod
    def find_sequence_board(board: np.array, sequence) -> bool:
        """
        Given a board, attempts to find a sequence in all possible directions
        :param board:
        :param sequence:
        :return: True if the sequence is in the board, False otherwise
        """
        for i in range(len(board)):
            # Check in lines
            if NeutreekoUtils.search_sequence_numpy(board[i, :], sequence):
                return True
            # check in columns
            if NeutreekoUtils.search_sequence_numpy(board[:, i], sequence):
                return True

        # check victory in diagonals
        flipped_board = np.fliplr(board)
        for i in range(-2, 3):
            diagonal1 = np.diagonal(board, offset=i)
            if NeutreekoUtils.search_sequence_numpy(diagonal1, sequence):
                return True
            diagonal2 = np.diagonal(flipped_board, offset=i)
            if NeutreekoUtils.search_sequence_numpy(diagonal2, sequence):
                return True

        return False

    @staticmethod
    def value_in_board(board, coords: Tuple[int, int]) -> int:
        """
        Returns the value in the board

        :param board: A np array of size (5,5)
        :param coords: The x and y coordinates of a spot
        :return: The integer value in the board
        """
        if (coords[0] < 0) | (coords[0] >= const.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= const.BOARD_SIZE):
            return False
        return board[coords[0], coords[1]]

    @staticmethod
    def replace_in_board(board, coords: Tuple[int, int], value: int) -> Union[None, bool]:
        """
        Replaces a value in the board

        :param board: A np array of size (5,5)
        :param coords: The x and y coordinates of a spot
        :param value: the value to be in the board
        :return: None or False if the coords are not valid
        """
        if (coords[0] < 0) | (coords[0] >= const.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= const.BOARD_SIZE):
            return False
        board[coords[0], coords[1]] = value
