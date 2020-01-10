
import enum
import random


# List of orientations
class Orientation(enum.Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


# List of colours
class Shape(enum.Enum):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Tetromino():

    coordinate_table = (
        [[0, 0], [0, 0], [0, 0], [0, 0]],
        [[0, -1], [0, 0], [-1, 0], [-1, 1]],
        [[0, -1], [0, 0], [1, 0], [1, 1]],
        [[0, -1], [0, 0], [0, 1], [0, 2]],
        [[-1, 0], [0, 0], [1, 0], [0, 1]],
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[-1, -1], [0, -1], [0, 0], [0, 1]],
        [[1, -1], [0, -1], [0, 0], [0, 1]]
    )

    def __init__(self, center):

        self.center = center
        self.orientation = Orientation.UP
        self.identity = Shape.NoShape
        self.coordinates = Tetromino.coordinate_table[0]

        self.random_assign_shape()

    def random_assign_shape(self):

        random_shape = random.randint(1, 7)
        self.identity = Shape(random_shape)
        self.coordinates = Tetromino.coordinate_table[random_shape]
        self.update_center(self.center[0], self.center[1])

    def update_center(self, x, y):

        self.center = (x, y)
        print(self.coordinates)
        temp_coordinates = []
        for positions in self.coordinates:
            temp_coordinates.append([positions[0] + x, positions[1] + y])
        self.coordinates = temp_coordinates

    def move_by(self, x, y):

        temp_coordinates = []
        for positions in self.coordinates:
            new_x = positions[0] + x
            new_y = positions[1] + y
            temp_coordinates.append([new_x, new_y])
        self.coordinates = temp_coordinates
