# Actions
import numpy

UP = (-1, 0)
DOWN = (+1, 0)
LEFT = (0, -1)
RIGHT = (0, +1)
UP_LEFT = (-1, -1)
UP_RIGHT = (-1, +1)
DOWN_LEFT = (+1, -1)
DOWN_RIGHT = (+1, +1)

# ACTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

ACTIONS_DICT = {'UP': (-1, 0),
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

BLACK_WIN = numpy.array([BLACK, BLACK, BLACK])
WHITE_WIN = numpy.array([WHITE, WHITE, WHITE])
