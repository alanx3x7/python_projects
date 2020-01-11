
from enum import IntEnum
import random

# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# List of orientations
class Orientation(IntEnum):
    SPAWN = 0
    RIGHT = 1
    TWO = 2
    LEFT = 3

    def next(self):
        new_index = self.value + 1
        if new_index > 3:
            new_index = 0
        return new_index

    def prev(self):
        new_index = self.value - 1
        if new_index < 0:
            new_index = 3
        return new_index


# List of colours
class Shape(IntEnum):
    NoShape = 0
    ZShape = 1
    SShape = 2
    IShape = 3
    TShape = 4
    OShape = 5
    LShape = 6
    JShape = 7


class Tetromino():

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

    def __init__(self, piece_center):

        self.center = piece_center
        self.orientation = Orientation.SPAWN
        self.identity = Shape.NoShape
        self.coordinates = Tetromino.coordinate_table[0][0]

        self.random_assign_shape()

    def random_assign_shape(self):

        value = random.randint(1, 7)
        self.identity = Shape(value)
        self.orientation = Orientation.SPAWN
        self.coordinates = Tetromino.coordinate_table[value][0]
        self.move_to_center()

    def update_center(self, x, y):
        self.center = (x, y)

    def move_to_center(self):
        temp_coordinates = []
        for positions in Tetromino.coordinate_table[self.identity.value][self.orientation.value]:
            temp_coordinates.append([positions[0] + self.center[0], positions[1] + self.center[1]])
        self.coordinates = temp_coordinates

    def move_by(self, x, y):
        self.update_center(self.center[0] + x, self.center[1] + y)
        self.move_to_center()

    def rotate(self):
        temp_coordinates = []
        for positions in Tetromino.coordinate_table[self.identity.value][self.orientation.value]:
            temp_coordinates.append([positions[0] + self.center[0], positions[1] + self.center[1]])
        self.coordinates = temp_coordinates

    def rotate_right(self):
        self.orientation = Orientation(self.orientation.next())
        self.rotate()

    def rotate_left(self):
        self.orientation = Orientation(self.orientation.prev())
        self.rotate()

    def wall_kick_offset(self, direction):
        table_num = 1 if self.identity.value == Shape.IShape else 0
        case_adjust = 0 if direction == 1 else -1
        case_num = (self.orientation.value * 2) + case_adjust
        return Tetromino.kick_table[table_num][case_num]

