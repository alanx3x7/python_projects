
from enum import IntEnum


class Direction(IntEnum):
    RIGHT = 0
    LEFT = -1


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


# List of shapes
class Shape(IntEnum):
    NoShape = 0
    ZShape = 1
    SShape = 2
    IShape = 3
    TShape = 4
    OShape = 5
    LShape = 6
    JShape = 7
