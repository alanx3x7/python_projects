# Binairo main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/03

# Typical imports
import random
import time
import numpy as np

# PyQt5 specific imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Importing the class file for the individual cells
from binairo_cell import Cell


class MainWindow(QMainWindow):

    switch_window = pyqtSignal()

    def __init__(self, x_board_size, y_board_size, num_cells_start, num_per_hint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Alan\'s Binairo'          # Name of the window to be opened
        self.setWindowTitle(self.title)         # Sets the name of the window to be the title

        self.board_x_size = x_board_size                  # Initializes the x size of the board (width)
        self.board_y_size = y_board_size                  # Initializes the y size of the board (height)
        self.num_initial_seed = num_cells_start
        self.num_added_per_hint = num_per_hint
        self.board = np.zeros((self.board_y_size, self.board_x_size))

        self.num_blanks = self.board_x_size * self.board_y_size
        self.game_status = 0
        self._timer_start_nsecs = 0
        self.recursive_timer = 0

        # Creates a widget object, a vertical box object, and a horizontal box object
        self.first_window = QWidget()
        vb = QVBoxLayout()
        hb_top = QHBoxLayout()
        hb_bottom = QHBoxLayout()

        # Create a button to reset the board
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.pressed.connect(self.reset_button_click)
        hb_top.addWidget(self.reset_button, 0, Qt.Alignment())

        # Create a status label
        self.game_state_label = QLabel()
        self.game_state_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.game_state_label.font()  # Sets the font
        f.setPointSize(10)
        f.setWeight(75)
        self.game_state_label.setFont(f)
        self.game_state_label.setText("Generating puzzle")
        hb_top.addWidget(self.game_state_label, 0, Qt.Alignment())  # Adds the status label to the horizontal box

        # Create a button to solve the board
        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setFixedSize(QSize(64, 32))
        self.solve_button.pressed.connect(self.solve_button_click)  # Links the click to self.button_click function
        hb_top.addWidget(self.solve_button, 0, Qt.Alignment())  # Adds the button to the horizontal box

        # Add the horizontal box to the vertical box
        vb.addLayout(hb_top)

        # Create a button to make it easier
        self.hint_button = QPushButton("Hint", self)
        self.hint_button.setFixedSize(QSize(64, 32))
        self.hint_button.pressed.connect(self.hint_button_click)
        hb_bottom.addWidget(self.hint_button, 0, Qt.Alignment())

        # Create the clock label (timer)
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.clock.setFont(f)
        self.clock.setText("Time: 000.000")
        hb_bottom.addWidget(self.clock, 0, Qt.Alignment())  # Adds the clock label to the horizontal box

        # Create the timer object to keep track of time
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)  # Connects the timer to self.update_timer
        self._timer.start(10)  # 1 second timer                 # Updates and calls self.update_timer every 10 ms
        self._timer_start_nsecs = 0

        # Create a board size label
        self.change_button = QPushButton("Change", self)
        self.change_button.setFixedSize(QSize(64, 32))
        self.change_button.clicked.connect(self.change_button_click)
        hb_bottom.addWidget(self.change_button, 0, Qt.Alignment())

        # Add the bottom horizontal box to the vertical box
        vb.addLayout(hb_bottom)

        # Create a grid layout to hold all of the cell objects for each cell
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        vb.addLayout(self.grid)  # Adds the grid to the vertical box

        # Sets the layout of the widget to be the vertical box and centers it
        self.first_window.setLayout(vb)
        self.setCentralWidget(self.first_window)

        # Initializes grid with cell objects and sets up the minefield
        self.init_map()
        self.show()

        QApplication.processEvents()

        self.set_up_board()
        self.game_state_label.setText("Play!")
        self.game_status = 1
        self._timer_start_nsecs = time.time()

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

    def clear_board(self):
        self.board = np.zeros((self.board_y_size, self.board_x_size))

    def set_up_board(self):

        positions = self.create_solvable_board()
        temp_board = self.board.copy()
        self.clear_board()

        for i in range(len(positions)):
            x, y = positions[i]
            w = self.grid.itemAtPosition(y, x).widget()
            w.selected_state = temp_board[y, x]
            w.is_seeded = True
            w.update()
            self.board[y, x] = temp_board[y, x]

    def create_solvable_board(self):

        can_be_solved = False
        counter = 0
        positions = []

        while not can_be_solved:
            counter += 1
            print("Generating board trial %d" % counter)

            positions = []
            self.clear_board()
            while len(positions) < self.num_initial_seed:
                x = random.randint(0, self.board_x_size - 1)
                y = random.randint(0, self.board_y_size - 1)
                if (x, y) not in positions:
                    random_state = random.choice([-1, 1])
                    self.board[y, x] = random_state
                    if not self.is_valid_board():
                        self.board[y, x] = 0
                    else:
                        positions.append((x, y))

            self.recursive_timer = time.time()
            if self.get_solution_to_board() is not None:
                can_be_solved = True

        return positions

    def get_solution_to_board(self):

        if not self.is_valid_board() or time.time() - self.recursive_timer > 5:
            return None

        for y in range(self.board_y_size):
            for x in range(self.board_x_size):
                if self.board[y, x] == 0:

                    temp_board = self.board.copy()
                    self.board[y, x] = 1
                    self.apply_heuristics()
                    solution = self.get_solution_to_board()

                    if solution is None:
                        self.board = temp_board.copy()
                        self.board[y, x] = -1
                        self.apply_heuristics()
                        solution = self.get_solution_to_board()

                        if solution is None:
                            self.board = temp_board.copy()
                            self.board[y, x] = 0

                    return solution

        return self.board

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
                elif c == -1:
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
                elif c == -1:
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

    def apply_heuristics(self):

        while True:
            temp_board = self.board.copy()
            self.apply_simple_heuristics()
            self.apply_number_heuristics()
            if np.array_equal(temp_board, self.board):
                break

    def apply_simple_heuristics(self):

        for y in range(self.board_y_size):
            for x in range(self.board_x_size):
                if self.board[y, x] == 0:

                    if x < self.board_x_size - 2:
                        if self.board[y, x + 1] == self.board[y, x + 2] != 0:
                            self.board[y, x] = -self.board[y, x + 1]

                    if x > 1:
                        if self.board[y, x - 2] == self.board[y, x - 1] != 0:
                            self.board[y, x] = -self.board[y, x - 1]

                    if y < self.board_y_size - 2:
                        if self.board[y + 1, x] == self.board[y + 2, x] != 0:
                            self.board[y, x] = -self.board[y + 1, x]

                    if y > 1:
                        if self.board[y - 1, x] == self.board[y - 2, x] != 0:
                            self.board[y, x] = -self.board[y - 1, x]

                    if 0 < x < self.board_x_size - 1:
                        if self.board[y, x - 1] == self.board[y, x + 1] != 0:
                            self.board[y, x] = -self.board[y, x + 1]

                    if 0 < y < self.board_y_size - 1:
                        if self.board[y - 1, x] == self.board[y + 1, x] != 0:
                            self.board[y, x] = -self.board[y + 1, x]

    def apply_number_heuristics(self):

        for y in range(self.board_y_size):
            num_white = np.count_nonzero(self.board[y, :] == 1)
            num_black = np.count_nonzero(self.board[y, :] == -1)
            if num_white == self.board_x_size / 2:
                for x in range(self.board_x_size):
                    if self.board[y, x] == 0:
                        self.board[y, x] = -1
            elif num_black == self.board_x_size / 2:
                for x in range(self.board_x_size):
                    if self.board[y, x] == 0:
                        self.board[y, x] = 1

        for x in range(self.board_x_size):
            num_white = np.count_nonzero(self.board[:, x] == 1)
            num_black = np.count_nonzero(self.board[:, x] == -1)
            if num_white == self.board_y_size / 2:
                for y in range(self.board_y_size):
                    if self.board[y, x] == 0:
                        self.board[y, x] = -1
            elif num_black == self.board_y_size / 2:
                for y in range(self.board_y_size):
                    if self.board[y, x] == 0:
                        self.board[y, x] = 1

    def cell_clicked(self, x, y, state):

        if self.board[y, x] == 0 and state != 0:
            self.num_blanks -= 1
        elif self.board[y, x] != 0 and state == 0:
            self.num_blanks += 1

        self.board[y, x] = state

        w = self.grid.itemAtPosition(y, x).widget()
        if not self.is_valid_board():
            w.is_valid = False
            w.update()
        else:
            w.is_valid = True
            w.update()

        num_blanks_remaining = self.board_x_size * self.board_y_size - np.count_nonzero(self.board)
        if num_blanks_remaining == 0 and self.is_valid_board():
            self.game_state_label.setText("Hooray!")
            self.game_status = 0
            for y in range(self.board_y_size):
                for x in range(self.board_x_size):
                    w = self.grid.itemAtPosition(y, x).widget()
                    w.is_seeded = True
                    w.update()

    def solve_button_click(self):

        self.game_state_label.setText("Solving")
        self.game_status = 0
        QApplication.processEvents()
        first_time = time.time()
        self.recursive_timer = time.time()
        solution = self.get_solution_to_board()
        print("Time taken to solve: %07.3f seconds" % (time.time() - first_time))

        if solution is None:
            self.game_state_label.setText("Cannot be solved")
        else:
            for y in range(self.board_y_size):
                for x in range(self.board_x_size):
                    w = self.grid.itemAtPosition(y, x).widget()
                    w.selected_state = solution[y, x]
                    w.is_seeded = True
                    w.update()
            self.game_state_label.setText("Solution")

    def reset_button_click(self):

        self.game_status = 0
        self.game_state_label.setText("Generating puzzle")
        for y in range(self.board_y_size):
            for x in range(self.board_x_size):
                self.grid.itemAtPosition(y, x).widget().reset_cell()

        QApplication.processEvents()

        self.clear_board()
        self.set_up_board()
        self.game_state_label.setText("Play!")
        self._timer_start_nsecs = time.time()
        self.game_status = 1

    def hint_button_click(self):

        self.game_status = 0                    # Pause the game so that the timer does not keep counting
        self.game_state_label.setText("Generating Hint")
        QApplication.processEvents()

        self.recursive_timer = time.time()
        temp_board = self.board.copy()
        num_blanks_remaining = self.board_x_size * self.board_y_size - np.count_nonzero(temp_board)
        solution = self.get_solution_to_board()

        if solution is not None:
            positions = []
            while len(positions) < min(num_blanks_remaining, self.num_added_per_hint):
                x = random.randint(0, self.board_x_size - 1)
                y = random.randint(0, self.board_y_size - 1)
                if temp_board[y, x] == 0:
                    temp_board[y, x] = solution[y, x]
                    w = self.grid.itemAtPosition(y, x).widget()
                    w.selected_state = solution[y, x]
                    w.is_seeded = True
                    w.update()
                    positions.append((x, y))

        self.board = temp_board
        if num_blanks_remaining <= self.num_added_per_hint:
            self.game_state_label.setText("Solution")
        else:
            self.game_state_label.setText("Play!")
            self.game_status = 1
            self._timer_start_nsecs += time.time() - self.recursive_timer

    def change_button_click(self):
        self.switch_window.emit()

    def update_timer(self):
        """ Called at the predetermined rate to update the timer label regularly
        """

        if self.game_status == 1:  # Only update timer when game is being played
            n_secs = time.time() - self._timer_start_nsecs  # Finds the time passed since the game started
            self.clock.setText("Time: %07.3f" % n_secs)  # Updates the timer label to display time elapsed
        else:
            self._timer_start_nsecs += 0.01
