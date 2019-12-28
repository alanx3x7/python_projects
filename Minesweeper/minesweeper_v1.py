import math
import sys

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
        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = Cell(x, y)
                self.grid.addWidget(w, y, x)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
