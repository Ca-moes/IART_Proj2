# Lógica do Jogo: https://github.com/towzeur/gym-abalone/blob/master/gym_abalone/game/engine/gamelogic.py
import numpy as np
from typing import Tuple, List, Union

from gym_neutreeko.game.common import const
from gym_neutreeko.game.common.gameutils import NeutreekoUtils as utils


class NeutreekoEasyGame:
    def __init__(self):
        self.board = None
        self.current_player = None
        self.game_over = None
        self.turns_count = None

    def reset(self):
        self.board = self.new_board()
        self.current_player = 1
        self.game_over = False
        self.turns_count = 0

    @staticmethod
    def new_board():
        """
        TODO: Caso seja um board já acabado, escolher outro
        returns a random starting board, each element is a numpy.int8 (-128, 127)

        :return: numpy.array
        """
        return np.array([[0, 1, 0, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]], dtype=np.int8)

        board = np.array([[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]], dtype=np.int8)
        piece_1_x = np.random.randint(0, 5)
        piece_1_y = np.random.randint(0, 5)

        piece_2_x = np.random.randint(0, 5)
        piece_2_y = np.random.randint(0, 5)
        while (piece_1_x == piece_2_x) & (piece_1_y == piece_2_y):
            piece_2_x = np.random.randint(0, 5)
            piece_2_y = np.random.randint(0, 5)

        piece_3_x = np.random.randint(0, 5)
        piece_3_y = np.random.randint(0, 5)
        while ((piece_1_x == piece_3_x) & (piece_1_y == piece_3_y)) | ((piece_2_x == piece_3_x) & (piece_2_y == piece_3_y)):
            piece_3_x = np.random.randint(0, 5)
            piece_3_y = np.random.randint(0, 5)

        board[piece_1_x][piece_1_y] = 1
        board[piece_2_x][piece_2_y] = 1
        board[piece_3_x][piece_3_y] = 1

        return board

    def value_in_board(self, position: Tuple[int, int]) -> int:
        """
        Returns the value in a position of the board

        :param position: Tuple with 2 ints representing the coordinates of a cell
        :return: The int value
        """
        return utils.value_in_board(self.board, position)

    def replace_in_board(self, position: Tuple[int, int], value: int) -> None:
        """
        Replaces a value in a board position
        :param position: Tuple with 2 ints representing the coordinates of a cell
        :param value: Value of a player
        :return: None
        """
        utils.replace_in_board(self.board, position, value)

    def free_cell(self, coords: Tuple[int, int]) -> bool:
        """
        Checks if a cell is within bounds of the board and is free (value is 0)

        :param coords: Tuple with 2 ints representing the coordinates of a cell
        :return: True if the cell equals 0 and is within bounds
        """
        if (coords[0] < 0) | (coords[0] >= const.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= const.BOARD_SIZE):
            return False
        value = self.value_in_board(coords)
        return value == 0

    def check_direction(self, coords: Tuple[int, int], direction: str) -> Union[None, Tuple[int, int]]:
        """
        Returns the resulting position given a starting position and a direction.
        If the direction is not valid, returns None

        :param coords: Coordinates of intial point
        :param direction: String representation of the direction to take
        :return: None if direction is not valid OR tuple with new coords of resulting positions
        """
        action_coords = const.EASY_ACTIONS_DICT[direction]
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

    def available_directions(self, coords: Tuple[int, int]) -> List[str]:
        """
        For some starting coords, returns a list of pairs directions-finishing_coords
        """
        dirs = []
        for action_name in const.EASY_ACTIONS_DICT.keys():
            result = self.check_direction(coords, action_name)
            if result:
                dirs.append(action_name)
        return dirs

    def get_possible_moves(self, player: int, only_valid: bool = False) -> List[int]:
        """
        Return all the possible moves for a given player with the current board

        :param player: Integer representing the player
        :param only_valid:
        :return: A list of tuples with the starting position and a direction
        """
        dirs_value = {
            'UP': 0,
            'DOWN': 1,
            'LEFT': 2,
            'RIGHT': 3
        }
        possible_moves = []

        # Find player piece positions
        result = np.where(self.board == player)
        list_of_coordinates = list(zip(result[0], result[1]))

        # for each player piece
        piece_value = 0
        for pos in list_of_coordinates:
            if only_valid:
                # checks which directions are available
                dirs = self.available_directions(pos)
                for dir in dirs:
                    value = 4*piece_value + dirs_value[dir]
                    possible_moves.append(value)
            else:
                # adds every direction
                for dir in const.EASY_ACTIONS_DICT.keys():
                    possible_moves.append(4*piece_value + dirs_value[dir])
            piece_value += 1
        return possible_moves

    def action_handler(self, pos, dir) -> Tuple[str, tuple, str]:
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

        self.update_game(pos, result)
        self.turns_count += 1

        self.game_over = utils.find_sequence_board(self.board, np.array([1, 1, 1]))

        move_type = "win" if self.game_over else "default"
        return dir, result, move_type

    def update_game(self, pos, result):
        self.replace_in_board(result, 1)
        self.replace_in_board(pos, 0)
        pass

    def render(self):
        print(self.board)


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
        return utils.value_in_board(self.board, position)

    def replace_in_board(self, position: Tuple[int, int], value: int) -> None:
        """
        Replaces a value in a board position
        :param position: Tuple with 2 ints representing the coordinates of a cell
        :param value: Value of a player
        :return: None
        """
        utils.replace_in_board(self.board, position, value)

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
        """
        dirs = []
        for action_name in const.ACTIONS_DICT.keys():
            result = self.check_direction(coords, action_name)
            if result:
                dirs.append(action_name)
        return dirs

    def get_possible_moves(self, player: int, only_valid: bool = False) -> List[tuple]:
        """
        Return all the possible moves for a given player with the current board

        :param player: Integer representing the player
        :param only_valid:
        :return: A list of tuples with the starting position and a direction
        """
        possible_moves = []

        # Find player piece positions
        result = np.where(self.board == player)
        list_of_coordinates = list(zip(result[0], result[1]))

        # for each player piece
        for pos in list_of_coordinates:
            if only_valid:
                # checks which directions are available
                dirs = self.available_directions(pos)
                for dir in dirs:
                    possible_moves.append((pos, dir))
            else:
                # adds every direction
                for direction in const.ACTIONS_DICT.keys():
                    possible_moves.append((pos, direction))
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

        self.update_game(pos, result)
        self.update_player_turns()

        white_win = utils.find_sequence_board(self.board, const.WHITE_WIN)
        black_win = utils.find_sequence_board(self.board, const.BLACK_WIN)

        self.game_over = (white_win or black_win)
        move_type = "win" if self.game_over else "default"
        return dir, result, move_type

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
