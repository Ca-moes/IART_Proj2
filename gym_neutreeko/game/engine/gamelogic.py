# Lógica do Jogo: https://github.com/towzeur/gym-abalone/blob/master/gym_abalone/game/engine/gamelogic.py
import numpy as np
from typing import Tuple, List, Union

from gym_neutreeko.game.common import const
from gym_neutreeko.game.common.gameutils import NeutreekoUtils as utils


class NeutreekoGame:

    def __init__(self):
        self.board = None
        self.current_player = None
        self.game_over = None
        self.turns_count = None

    def reset(self):
        self.board = self.new_board()
        self.current_player = const.BLACK
        self.game_over = False
        self.turns_count = 0

    @staticmethod
    def new_board():
        """
        returns a fresh starting board, each element is a numpy.int8 (-128, 127)

        :return: numpy.array
        """
        return np.array([[0, 1, 0, 1, 0],
                         [0, 0, 2, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 2, 0, 2, 0]], dtype=np.int8)

    def value_in_board(self, position: Tuple[int, int]) -> int:
        """
        Returns the value in a position of the board

        :param position: Tuple with 2 ints representing the coordinates of a cell
        :return: The int value
        """
        return self.board[position[0], position[1]]

    def replace_in_board(self, position: Tuple[int, int], value: int) -> None:
        """
        Replaces a value in a board position
        :param position: Tuple with 2 ints representing the coordinates of a cell
        :param value: Value of a player
        :return: None
        """
        self.board[position[0], position[1]] = value

    def free_cell(self, coords: Tuple[int, int]) -> bool:
        """
        Checks if a cell is within bounds of the board and is free (value is 0)

        :param coords: Tuple with 2 ints representing the coordinates of a cell
        :return: True if the cell equals 0 and is within bounds
        """
        if (coords[0] < 0) | (coords[0] >= const.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= const.BOARD_SIZE):
            return False
        value = self.board[coords[0]][coords[1]]
        return value == 0

    def check_direction(self, coords: Tuple[int, int], direction: str) -> Union[None, Tuple[int, int]]:
        """
        Returns the resulting position given a starting position and a direction.
        If the direction is not valid, returns None

        :param coords: Coordinates of intial point
        :param direction: String representation of the direction to take
        :return: None if direction is not valid OR tuple with new coords of resulting positions
        """
        action_coords = const.ACTIONS_DICT[direction]
        attempt_coords = tuple(np.add(coords, action_coords))
        free_cell = self.free_cell(attempt_coords)
        if not free_cell:
            return None
        # apply direction until it reaches EOB (end of board) or another piece
        while free_cell:
            new_coords = attempt_coords
            attempt_coords = tuple(np.add(new_coords, action_coords))
            free_cell = self.free_cell(attempt_coords)
        return new_coords

    def available_directions(self, coords: Tuple[int, int]) -> List[Tuple[str, tuple]]:
        """
        For some starting coords, returns a list of pairs directions-finishing_coords
        FIXME: untested inside for loop, need to check if "check_direction" is working as intended
        """
        dirs = []
        for action_name in const.ACTIONS_DICT.keys():
            result = self.check_direction(coords, action_name)
            if result:
                dirs.append(result)
        return dirs

    def get_possible_moves(self, player: int, only_valid: bool = False) -> List[tuple]:
        """
        Return all the possible moves for a given player with the current board

        :param player: Integer representing the player
        :param only_valid: TODO Boolean to be used in the future
        :return: A list of tuples with the starting position and a direction
        """
        if only_valid:
            raise Exception("Not yet implemented")

        possible_moves = []

        result = np.where(self.board == player)
        list_of_coordinates = list(zip(result[0], result[1]))
        for pos in list_of_coordinates:
            for direction in const.ACTIONS_DICT.keys():
                possible_moves.append((pos, direction))

        return possible_moves

    def OLD_get_possible_moves(self, player: int) -> list:
        """
        Este método já dá as moves válidos. Pode ser usado mais tarde
        Será usado no método acima

        :param player: Valor inteiro do jogador que vai jogar
        :return:
        """
        # Encontra peças do player
        result = np.where(self.board == player)
        listOfCoordinates = list(zip(result[0], result[1]))
        # Vê quais as direções válidas para essa peça (função à parte para fazer)
        possible_moves = []
        for coords in listOfCoordinates:
            dirs = self.available_directions(coords)
            possible_moves.append((coords, dirs))
        return possible_moves

    def action_handler(self, pos, dir):
        """
        After the agent chooses a move, it needs to be checked to see if it's valid
        If it is valid, returns new position

        :param pos: The position of the piece that will be moved
        :param dir: The direction that the piece will be moved to
        :return:
        """
        result = self.check_direction(pos, dir)
        if not result:
            return None

        self.update_player_turns()
        self.update_game(pos, result)

        self.game_over = self.check_endgame()
        return dir, result

    def update_player_turns(self):
        self.current_player = const.WHITE if self.current_player == const.BLACK else const.BLACK
        self.turns_count += 1

    def update_game(self, pos, result):
        player = self.value_in_board(pos)
        self.replace_in_board(result, player)
        self.replace_in_board(pos, 0)
        pass

    def render(self):
        print(self.board)

    def check_endgame(self) -> bool:

        for i in range(const.BOARD_SIZE):
            # Check victory in lines
            if self.check_endgame_array(self.board[i, :]):
                return True
            # check victory in columns
            if self.check_endgame_array(self.board[:, i]):
                return True

        # check victory in diagonals
        flipped_board = np.fliplr(self.board)
        for i in range(-2, 3):
            diagonal1 = np.diagonal(self.board, offset=i)
            if self.check_endgame_array(diagonal1):
                return True
            diagonal2 = np.diagonal(flipped_board, offset=i)
            if self.check_endgame_array(diagonal2):
                return True

        return False

    def check_endgame_array(self, array) -> bool:
        win1 = utils.search_sequence_numpy(array, const.BLACK_WIN)
        win2 = utils.search_sequence_numpy(array, const.WHITE_WIN)
        return win1 or win2
