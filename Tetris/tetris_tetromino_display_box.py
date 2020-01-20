# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TetrominoDisplay(QWidget):
    coordinate_table = (
        # No Shape
        [[0, 0], [0, 0], [0, 0], [0, 0]],

        # Z Shape
        [[0, 0], [0, 1], [1, 1], [1, 2]],

        # S Shape
        [[1, 0], [1, 1], [0, 1], [0, 2]],

        # I Shape
        [[0.5, -0.5], [0.5, 0.5], [0.5, 1.5], [0.5, 2.5]],

        # T Shape
        [[1, 0], [1, 1], [1, 2], [0, 1]],

        # O Shape
        [[0, 0.5], [0, 1.5], [1, 0.5], [1, 1.5]],

        # L Shape
        [[1, 0], [1, 1], [1, 2], [0, 2]],

        # J Shape
        [[0, 0], [1, 0], [1, 1], [1, 2]]
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.identity = None

        self.width = 5
        self.height = 3

        self.cell_side_length = 30

        self.colour_table = [0x000000, 0xFF0000, 0x00FF00, 0x00FFFF, 0x800080, 0xFFFF00, 0xFFA500, 0x0000FF]

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.paintBackground(p)

        if self.identity is not None:
            self.paintPiece(p)

    def paintBackground(self, p):
        p.setPen(QPen(Qt.black, 0, Qt.SolidLine))
        p.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        p.drawRect(0, 0, self.cell_side_length * self.width, self.cell_side_length * self.height)

    def paintPiece(self, p):
        p.setPen(QPen(Qt.black, 0, Qt.SolidLine))
        p.setBrush(QBrush(QColor(self.colour_table[self.identity.value]), Qt.SolidPattern))

        for positions in TetrominoDisplay.coordinate_table[self.identity.value]:
            x = (positions[1] + 1) * self.cell_side_length
            y = (positions[0] + 0.5) * self.cell_side_length
            p.drawRect(x, y, 30, 30)

    def update_identity(self, piece):
        self.identity = piece
        self.update()
