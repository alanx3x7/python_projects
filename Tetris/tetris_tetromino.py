
import random

from tetris_enums import Shape
from tetris_enums import Orientation


class Tetromino:

    coordinate_table = (
        # No Shape
        [[[0, 0],   [0, 0],     [0, 0],     [0, 0]],
         [[0, 0],   [0, 0],     [0, 0],     [0, 0]],
         [[0, 0],   [0, 0],     [0, 0],     [0, 0]],
         [[0, 0],   [0, 0],     [0, 0],     [0, 0]]],

        # Z Shape
        [[[-1, -1],  [0, -1],    [0, 0],     [1, 0]],
         [[1, -1],   [1, 0],     [0, 0],     [0, 1]],
         [[1, 1],    [0, 1],     [0, 0],     [-1, 0]],
         [[-1, 1],   [-1, 0],    [0, 0],     [0, -1]]],

        # S Shape
        [[[-1, 0],   [0, 0],     [0, -1],    [1, -1]],
         [[0, -1],   [0, 0],     [1, 0],     [1, 1]],
         [[1, 0],    [0, 0],     [0, 1],     [-1, 1]],
         [[0, 1],    [0, 0],     [-1, 0],    [-1, -1]]],

        # I Shape
        [[[-1, 0],   [0, 0],     [1, 0],     [2, 0]],
         [[1, -1],   [1, 0],     [1, 1],     [1, 2]],
         [[-1, 1],   [0, 1],     [1, 1],     [2, 1]],
         [[0, -1],   [0, 0],     [0, 1],     [0, 2]]],

        # T Shape
        [[[-1, 0],   [0, 0],     [1, 0],     [0, -1]],
         [[0, -1],   [0, 0],     [0, 1],     [1, 0]],
         [[1, 0],    [0, 0],     [-1, 0],    [0, 1]],
         [[0, 1],    [0, 0],     [0, -1],    [-1, 0]]],

        # O Shape
        [[[0, 0],    [1, 0],     [0, -1],    [1, -1]],
         [[0, 0],    [1, 0],     [0, -1],    [1, -1]],
         [[0, 0],    [1, 0],     [0, -1],    [1, -1]],
         [[0, 0],    [1, 0],     [0, -1],    [1, -1]]],

        # L Shape
        [[[-1, 0],   [0, 0],     [1, 0],     [1, -1]],
         [[0, -1],   [0, 0],     [0, 1],     [1, 1]],
         [[1, 0],    [0, 0],     [-1, 0],    [-1, 1]],
         [[0, 1],    [0, 0],     [0, -1],    [-1, -1]]],

        # J Shape
        [[[-1, -1],  [-1, 0],    [0, 0],     [1, 0]],
         [[1, -1],   [0, -1],    [0, 0],     [0, 1]],
         [[1, 1],    [1, 0],     [0, 0],     [-1, 0]],
         [[-1, 1],   [0, 1],     [0, 0],     [0, -1]]]
    )

    kick_table = (
        # J, L, S, T, Z Shape
        [[[0, 0], [-1, 0], [-1, +1], [0, -2], [-1, -2]],    # 0 -> R
         [[0, 0], [+1, 0], [+1, -1], [0, +2], [+1, +2]],    # R -> 0
         [[0, 0], [+1, 0], [+1, -1], [0, +2], [+1, +2]],    # R -> 2
         [[0, 0], [-1, 0], [-1, +1], [0, -2], [-1, -2]],    # 2 -> R
         [[0, 0], [+1, 0], [+1, +1], [0, -2], [+1, -2]],    # 2 -> L
         [[0, 0], [-1, 0], [-1, -1], [0, +2], [-1, +2]],    # L -> 2
         [[0, 0], [-1, 0], [-1, -1], [0, +2], [-1, +2]],    # L -> 0
         [[0, 0], [+1, 0], [+1, +1], [0, -2], [+1, -2]]],   # 0 -> L

        # I Shape
        [[[0, 0], [-2, 0], [+1, 0], [-2, -1], [+1, +2]],
         [[0, 0], [+2, 0], [-1, 0], [+2, +1], [-1, -2]],
         [[0, 0], [-1, 0], [+2, 0], [-1, +2], [+2, -1]],
         [[0, 0], [+1, 0], [-2, 0], [+1, -2], [-2, +1]],
         [[0, 0], [+2, 0], [-1, 0], [+2, +1], [-1, -2]],
         [[0, 0], [-2, 0], [+1, 0], [-2, -1], [+1, +2]],
         [[0, 0], [+1, 0], [-2, 0], [+1, -2], [-2, +1]],
         [[0, 0], [-1, 0], [+2, 0], [-1, +2], [+2, -1]]]
    )

    def __init__(self, piece_center, shape=None):

        self.center = piece_center
        self.orientation = Orientation.SPAWN

        if shape is None:
            self.identity = Shape.NoShape
            self.coordinates = Tetromino.coordinate_table[0][0]
            self.random_assign_shape()
        else:
            self.identity = shape
            self.coordinates = Tetromino.coordinate_table[shape.value][0]
            self.move_to_center()

    def random_assign_shape(self):
        value = random.randint(1, 7)
        self.identity = Shape(value)
        self.coordinates = Tetromino.coordinate_table[value][0]
        self.move_to_center()

    def update_center(self, x, y):
        self.center = (x, y)

    def move_to_center(self):
        self.coordinates = []
        for positions in Tetromino.coordinate_table[self.identity.value][self.orientation.value]:
            self.coordinates.append([positions[0] + self.center[0], positions[1] + self.center[1]])

    def move_by(self, x, y):
        self.update_center(self.center[0] + x, self.center[1] + y)
        self.move_to_center()

    def move_to(self, new_center, new_positions):
        self.update_center(new_center[0], new_center[1])
        self.coordinates = new_positions

    def rotate(self):
        self.coordinates = []
        for positions in Tetromino.coordinate_table[self.identity.value][self.orientation.value]:
            self.coordinates.append([positions[0] + self.center[0], positions[1] + self.center[1]])

    def rotate_right(self):
        self.orientation = Orientation(self.orientation.next())
        self.rotate()

    def rotate_left(self):
        self.orientation = Orientation(self.orientation.prev())
        self.rotate()

    def wall_kick_offset(self, direction):
        table_num = 1 if self.identity.value == Shape.IShape else 0
        case_adjust = direction.value
        case_num = (self.orientation.value * 2) + case_adjust
        return Tetromino.kick_table[table_num][case_num]

    def __copy__(self):
        tetromino_copy = Tetromino(self.center)
        tetromino_copy.identity = self.identity
        tetromino_copy.orientation = self.orientation
        tetromino_copy.coordinates = self.coordinates
        return tetromino_copy
