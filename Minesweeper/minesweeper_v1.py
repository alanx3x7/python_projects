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
        self.mines_left = self.num_mines
        self.setWindowTitle(self.title)
        self.first_already_clicked = False
        self.num_cells_clicked = 0

        w = QWidget()
        vb = QVBoxLayout()

        hb = QHBoxLayout()

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.pressed.connect(self.button_click)
        hb.addWidget(self.reset_button)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.clock.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.clock.setFont(f)
        self.clock.setText("000")
        hb.addWidget(self.clock)

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.mines.setFont(f)
        self.mines.setText("%03d" % self.num_mines)
        hb.addWidget(self.mines)

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
                w.clicked.connect(self.cell_clicked)
                w.expandable.connect(self.expand_reveal)
                w.oh_no.connect(self.game_over)
                w.double_clicked.connect(self.expand_dc_reveal)
                w.flagged.connect(self.cell_flagged)

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

    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine:
                    w.click()

    def expand_dc_reveal(self, x, y):
        t = self.grid.itemAtPosition(y, x).widget()

        flags_adjacent = 0
        for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if w.is_flagged:
                    flags_adjacent = flags_adjacent + 1

        if flags_adjacent == t.num_adjacent:
            for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
                for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                    w = self.grid.itemAtPosition(yi, xi).widget()
                    if not w.is_flagged:
                        w.reveal()

    def game_over(self):
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reveal()
        self.clock.setText("Failed!")

    def button_click(self):

        self.first_already_clicked = False

        # Clear all mine positions
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset_cell()

        self.set_up_map()
        self.mines_left = self.num_mines
        self.clock.setText("000")
        self.mines.setText("%03d" % self.mines_left)

    def cell_clicked(self, x, y):

        if not self.first_already_clicked:
            t = self.grid.itemAtPosition(y, x).widget()
            print(t.num_adjacent)
            while t.num_adjacent != 0:
                print("Redoing")
                self.button_click()
                t = self.grid.itemAtPosition(y, x).widget()
                print("Num adjacent %d at (%d, %d)" % (t.num_adjacent, x, y))
            self.first_already_clicked = True
            t.click()

        num_clicked = 0
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                if w.is_revealed:
                    num_clicked = num_clicked + 1
        if num_clicked == self.board_x_size * self.board_y_size - self.num_mines:
            self.clock.setText("Hooray!")

    def cell_flagged(self, x, y, add):

        t = self.grid.itemAtPosition(y, x).widget()
        self.mines_left = self.mines_left - add
        self.mines.setText("%03d" % self.mines_left)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
