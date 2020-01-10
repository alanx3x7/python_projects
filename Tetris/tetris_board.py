# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np


class TetrisBoard(QWidget):

    def __init__(self):

        super().__init__()

        self.width = 10
        self.height = 20
        self.cell_side_length = 30

        self.x_cell_corners = np.zeros(10)
        for x in range(self.width):
            self.x_cell_corners[x] = x * self.cell_side_length + 5

        self.y_cell_corners = np.zeros(20)
        for y in range(self.height):
            self.y_cell_corners[y] = y * self.cell_side_length + 5

    def paintEvent(self, event):

        # Creates the painter object and does things to it
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        p.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        for y in range(self.height):
            for x in range(self.width):
                p.drawRect(self.x_cell_corners[x], self.y_cell_corners[y], 30, 30)

