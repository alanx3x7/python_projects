# Binairo main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/03

# Typical imports
import sys
import random
import time
import numpy as np

# PyQt5 specific imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Importing the class file for the individual cells
from binairo_cell import Cell


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Binairo'          # Name of the window to be opened
        self.setWindowTitle(self.title)         # Sets the name of the window to be the title

        self.board_x_size = 14                  # Initializes the x size of the board (width)
        self.board_y_size = 14                  # Initializes the y size of the board (height)
        self.board = np.zeros((self.board_y_size, self.board_x_size))

        self.num_blanks = self.board_x_size * self.board_y_size
        self.game_status = 0
        self._timer_start_nsecs = 0

        # Creates a widget object, a vertical box object, and a horizontal box object
        w = QWidget()
        vb = QVBoxLayout()
        hb = QHBoxLayout()

        # Create a grid layout to hold all of the cell objects for each cell
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        vb.addLayout(self.grid)  # Adds the grid to the vertical box

        # Sets the layout of the widget to be the vertical box and centers it
        w.setLayout(vb)
        self.setCentralWidget(w)

        # Initializes grid with cell objects and sets up the minefield
        self.init_map()
        # self.set_up_map()

        # Displays the window
        self.show()

    def init_map(self):

        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):

                # Creates a cell object and add it to the grid at position (y, x)
                w = Cell(x, y)
                self.grid.addWidget(w, y, x)

                # Connect the signals for each cell to the respective functions
                w.clicked.connect(self.cell_clicked)                # Called when cell is clicked

    # def set_up_map(self):
    #
    #     while not self.valid_board():
    #         positions = []
    #         for x in range(0, self.board_x_size):
    #             for y in range(0, self.board_y_size):
    #                 w =

    # def get_solution_to_board(self):


    def is_valid_board(self):

        if not self.has_valid_rows() or not self.has_valid_cols():
            return False

        if not self.has_valid_adjacent_rows() or not self.has_valid_adjacent_cols():
            return False

        if not self.has_no_repeated_rows() or not self.has_no_repeated_cols():
            return False

        return True

    def has_valid_rows(self):

        for y in range(self.board_y_size):
            num_white = 0
            num_black = 0

            for x in range(self.board_x_size):
                c = self.board[y, x]

                if c == 1:
                    num_white += 1
                elif c == 2:
                    num_black += 1

            if num_black > self.board_x_size / 2 or num_white > self.board_y_size / 2:
                return False

        return True

    def has_valid_cols(self):

        for x in range(self.board_x_size):
            num_white = 0
            num_black = 0

            for y in range(self.board_y_size):
                c = self.board[y, x]

                if c == 1:
                    num_white += 1
                elif c == 2:
                    num_black += 1

            if num_black > self.board_x_size / 2 or num_white > self.board_y_size / 2:
                return False

        return True

    def has_valid_adjacent_rows(self):

        for y in range(self.board_y_size):
            for x in range(2, self.board_x_size):
                c = self.board[y, x]
                b = self.board[y, x - 1]
                a = self.board[y, x - 2]

                if a == b and a != 0:
                    if b == c:
                        return False

        return True

    def has_valid_adjacent_cols(self):

        for x in range(self.board_x_size):
            for y in range(2, self.board_y_size):
                c = self.board[y, x]
                b = self.board[y - 1, x]
                a = self.board[y - 2, x]

                if a == b and a != 0:
                    if b == c:
                        return False

        return True

    def has_no_repeated_rows(self):

        for i in range(self.board_y_size):
            for j in range(i + 1, self.board_y_size):
                same = True
                for k in range(self.board_x_size):
                    a = self.board[i, k]
                    b = self.board[j, k]
                    if a == 0 or a != b:
                        same = False
                        break
                if same:
                    return False

        return True

    def has_no_repeated_cols(self):

        for i in range(self.board_x_size):
            for j in range(i + 1, self.board_x_size):
                same = True
                for k in range(self.board_y_size):
                    a = self.board[k, i]
                    b = self.board[k, j]
                    if a == 0 or a != b:
                        same = False
                        break
                if same:
                    return False

        return True

    def cell_clicked(self, x, y, state):

        if self.board[y, x] == 0 and state != 0:
            self.num_blanks -= 1
        elif self.board[y, x] != 0 and state == 0:
            self.num_blanks += 1

        self.board[y, x] = state

        now = time.time()
        self.is_valid_board()
        print(time.time() - now)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
