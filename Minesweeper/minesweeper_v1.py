import math
import sys
import random

import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from minesweeper_cell_v1 import Cell


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Alan\'s Minesweeper'
        self.board_x_size = 20
        self.board_y_size = 10
        self.num_mines = 30
        self.setWindowTitle(self.title)

        w = QWidget()
        vb = QVBoxLayout()

        hb = QHBoxLayout()
        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        hb.addWidget(self.button)
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        vb.addLayout(self.grid)

        w.setLayout(vb)

        self.setCentralWidget(w)
        self.init_map()
        self.set_up_map()
        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = Cell(x, y)
                self.grid.addWidget(w, y, x)

    def set_up_map(self):

        positions = []
        while len(positions) < self.num_mines:
            x = random.randint(0, self.board_x_size - 1)
            y = random.randint(0, self.board_y_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                positions.append((x, y))

        # Add adjacencies to the positions
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.num_adjacent = self.get_adjacency_n(x, y)
                print(w.num_adjacent)

    def get_adjacency_n(self, x, y):
        positions = self.get_surrounding(x, y)
        n_mines = sum(1 if w.is_mine else 0 for w in positions)

        return n_mines

    def get_surrounding(self, x, y):
        positions = []

        for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())

        return positions


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
