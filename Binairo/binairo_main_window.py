# Binairo main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/07

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
    """ Main class window for the binairo game
    """

    # Signal when the button to edit board size and difficulty is pressed
    switch_window = pyqtSignal()

    def __init__(self, x_board_size, y_board_size, num_cells_start, num_per_hint, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Binairo'              # Name of the window to be opened
        self.setWindowTitle(self.title)             # Sets the name of the window to be the title

        self.board_x_size = x_board_size            # Initializes the x size of the board (width)
        self.board_y_size = y_board_size            # Initializes the y size of the board (height)

        # Works out the optimal number of cells to seed as 23% (determined experimentally)
        self.num_initial_seed = int(self.board_x_size * self.board_y_size * 0.23)
        self.num_cells_start = max(num_cells_start, self.num_initial_seed)          # Number of starting by difficulty
        self.num_added_per_hint = num_per_hint      # Number of cells added per hint button press

        # Creates a board as a numpy 2D array of ints, and creates variable to keep track of number of blanks
        self.board = np.zeros((self.board_y_size, self.board_x_size))
        self.num_blanks = self.board_x_size * self.board_y_size

        # Sets up game variables
        self.game_status = 0                        # 0 if not playing, 1 if playing
        self._timer_start_nsecs = 0                 # Timer displayed to user
        self.recursive_timer = 0                    # Timer to prevent recursion from taking too long

        # Creates a widget object, a vertical box object, and a horizontal box object
        self.first_window = QWidget(*args, **kwargs)
        vb = QVBoxLayout()                          # Main box that the layout will be set to
        hb_top = QHBoxLayout()                      # Top box holding the reset and solve buttons and game status
        hb_bot = QHBoxLayout()                   # Bottom box holding the hint and change buttons and game time

        # Create a button to reset the board
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.pressed.connect(self.reset_button_click)  # Links the click to self.reset_button_click
        hb_top.addWidget(self.reset_button, 0, Qt.Alignment())      # Adds the button to the horizontal box

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
        self.solve_button.pressed.connect(self.solve_button_click)  # Links the click to self.solve_button_click
        hb_top.addWidget(self.solve_button, 0, Qt.Alignment())      # Adds the button to the horizontal box

        # Add the horizontal box to the vertical box
        vb.addLayout(hb_top)

        # Create a button to make it easier
        self.hint_button = QPushButton("Hint", self)
        self.hint_button.setFixedSize(QSize(64, 32))
        self.hint_button.pressed.connect(self.hint_button_click)    # Links the click to self.hint_button_click
        hb_bot.addWidget(self.hint_button, 0, Qt.Alignment())       # Adds the button to the horizontal box

        # Create the clock label (timer)
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.clock.setFont(f)
        self.clock.setText("Time: 000.000")
        hb_bot.addWidget(self.clock, 0, Qt.Alignment())             # Adds the clock label to the horizontal box

        # Create the timer object to keep track of time
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)              # Connects the timer to self.update_timer
        self._timer.start(10)                                       # Updates and calls self.update_timer every 10 ms
        self._timer_start_nsecs = 0

        # Create a board size label
        self.change_button = QPushButton("Change", self)
        self.change_button.setFixedSize(QSize(64, 32))
        self.change_button.clicked.connect(self.change_click)       # Connects button to self.change_click
        hb_bot.addWidget(self.change_button, 0, Qt.Alignment())     # Adds the change button to the horizontal box

        # Add the bottom horizontal box to the vertical box
        vb.addLayout(hb_bot)

        # Create a grid layout to hold all of the cell objects for each cell
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        vb.addLayout(self.grid)  # Adds the grid to the vertical box

        # Sets the layout of the widget to be the vertical box and centers it
        self.first_window.setLayout(vb)
        self.setCentralWidget(self.first_window)

        # Initializes grid with cell objects
        self.init_map()
        self.show()

        # Shows the user the generating window first so that they know the program is running
        QApplication.processEvents()

        # Sets up the board and updates the status label and tracker, and starts the timer
        self.set_up_board()
        self.game_state_label.setText("Play!")
        self.game_status = 1
        self._timer_start_nsecs = time.time()

        # Displays the window
        self.show()

    def init_map(self):
        """ Initializes the grid to be filled with binairo cell objects
        """

        # Iterates through all cells in the grid
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):

                # Creates a cell object and add it to the grid at position (y, x)
                w = Cell(x, y)
                self.grid.addWidget(w, y, x)

                # Connect the signals for each cell to the respective functions
                w.clicked.connect(self.cell_clicked)                # Called when cell is clicked

    def clear_board(self):
        """ Clears the board variable that keeps track of each cell state
        """
        self.board = np.zeros((self.board_y_size, self.board_x_size))

    def set_up_board(self):
        """ Sets up the binairo board with a new, unsolved puzzle
        """

        # Find the positions to be filled in to create a solvable board
        positions = self.create_solvable_board()
        temp_board = self.board.copy()

        # Clear the board so that only the starting cells are filled
        self.clear_board()

        # Goes through the positions one by one
        for i in range(len(positions)):
            x, y = positions[i]
            w = self.grid.itemAtPosition(y, x).widget()     # Finds the corresponding widget cell object
            w.selected_state = temp_board[y, x]             # Sets it to the correct state
            w.is_seeded = True                              # Sets it as a seeded cell
            w.update()                                      # Updates the appearance
            self.board[y, x] = temp_board[y, x]             # Updates the self.board as well

    def create_solvable_board(self):
        """ Finds the positions and states to fill in to create a solvable binairo board
        :return positions: A list of positions to be filled in to create a solvable board
        """

        # Initialize conditions and counters
        can_be_solved = False
        counter = 0
        positions = []

        # Loop until we create a board that can be solved
        while not can_be_solved:

            # Update counter and display status
            counter += 1
            print("Generating board trial %d" % counter)

            # Clears the board to generate a new one that is solvable
            positions = []
            self.clear_board()

            # First seed num_initial_seed randomly and sees if this is solvable
            while len(positions) < self.num_initial_seed:
                x = random.randint(0, self.board_x_size - 1)
                y = random.randint(0, self.board_y_size - 1)

                # Makes sure that the same position is not chosen twice
                if (x, y) not in positions:
                    random_state = random.choice([-1, 1])
                    self.board[y, x] = random_state

                    # If the random point makes the board invalid, we try again
                    if not self.is_valid_board():
                        self.board[y, x] = 0
                    else:
                        positions.append((x, y))

            # We try and find the solution to the board
            self.recursive_timer = time.time()          # We reset the timer to limit each solution to be 5 seconds
            solution = self.get_solution_to_board()

            # If a solution is possible, we exit the loop
            if solution is not None:
                can_be_solved = True

        # We then add a few more positions so that the number of starting positions matches the difficulty selected
        while len(positions) < self.num_cells_start:
            x = random.randint(0, self.board_x_size - 1)
            y = random.randint(0, self.board_y_size - 1)
            if (x, y) not in positions:
                positions.append((x, y))

        return positions

    def get_solution_to_board(self):
        """ Recursively finds the solution give the current self.board
        :return solution: The solution to the current board, none if no solution
        """

        # Base case, if the board is not valid or the time exceeds the maximum allowed time
        # We return no solution
        if not self.is_valid_board() or time.time() - self.recursive_timer > 5:
            return None

        # Loops through all positions of the board to find the next blank space
        for y in range(self.board_y_size):
            for x in range(self.board_x_size):
                if self.board[y, x] == 0:

                    # First make a copy of the current board
                    temp_board = self.board.copy()

                    # Tries to fill in with a white circle, and recursively sees if a solution is possible
                    self.board[y, x] = 1
                    self.apply_heuristics()
                    solution = self.get_solution_to_board()

                    # If the solution is not possible, we reset the board to the copy, and try with a black circle
                    if solution is None:
                        self.board = temp_board.copy()
                        self.board[y, x] = -1
                        self.apply_heuristics()
                        solution = self.get_solution_to_board()

                        # If neither white nor black circle works, we reset the board, and return as this path
                        # is invalid
                        if solution is None:
                            self.board = temp_board.copy()
                            self.board[y, x] = 0

                    return solution

        # If no blank space remains and board is valid, we have found the solution, and return the solution
        return self.board

    def is_valid_board(self):
        """ Checks that the board is valid as is
        :return boolean: True if the board is valid, False otherwise
        """

        # Checks whether there are the right number of black or white circles in each row and column
        if not self.has_valid_rows() or not self.has_valid_cols():
            return False

        # Checks if there are circles that are the same three in a row or column
        if not self.has_valid_adjacent_rows() or not self.has_valid_adjacent_cols():
            return False

        # Checks if there are any repeated rows or columns
        if not self.has_no_repeated_rows() or not self.has_no_repeated_cols():
            return False

        return True

    def has_valid_rows(self):
        """ Checks if the number of white or black circles are valid per each row
        :return boolean: True if valid, false otherwise
        """

        # Loops through each row
        for y in range(self.board_y_size):
            num_white = 0
            num_black = 0

            # Counts the number of white and black circles in each row
            for x in range(self.board_x_size):
                c = self.board[y, x]

                if c == 1:
                    num_white += 1
                elif c == -1:
                    num_black += 1

            # Row is invalid if the number of black or white exceeds half the row length
            if num_black > self.board_x_size / 2 or num_white > self.board_y_size / 2:
                return False

        return True

    def has_valid_cols(self):
        """ Checks if the number of white or black circles are valid per each column
        :return boolean: True if valid, false otherwise
        """

        # Loops through each column
        for x in range(self.board_x_size):
            num_white = 0
            num_black = 0

            # Counts the number of white and black circles in each column
            for y in range(self.board_y_size):
                c = self.board[y, x]

                if c == 1:
                    num_white += 1
                elif c == -1:
                    num_black += 1

            # Column is invalid if the number of black or white exceeds half the column length
            if num_black > self.board_x_size / 2 or num_white > self.board_y_size / 2:
                return False

        return True

    def has_valid_adjacent_rows(self):
        """ Checks whether there are instances where three of the same colour circle appears consecutively row-wise
        :return boolean: True if valid, False otherwise
        """

        # Loops through each row
        for y in range(self.board_y_size):

            # Checks if three consecutive are not blank and have the same colour
            for x in range(2, self.board_x_size):
                c = self.board[y, x]
                b = self.board[y, x - 1]
                a = self.board[y, x - 2]

                if a == b and a != 0:
                    if b == c:
                        return False

        return True

    def has_valid_adjacent_cols(self):
        """ Checks whether there are instances where three of the same colour circle appears consecutively column-wise
        :return boolean: True if valid, False otherwise
        """

        # Loops through each column
        for x in range(self.board_x_size):

            # Checks if three consecutive are not blank and have the same colour
            for y in range(2, self.board_y_size):
                c = self.board[y, x]
                b = self.board[y - 1, x]
                a = self.board[y - 2, x]

                if a == b and a != 0:
                    if b == c:
                        return False

        return True

    def has_no_repeated_rows(self):
        """ Checks whether rows are repeated
        :return boolean: True if no rows are repeated, False otherwise
        """

        # Loops through each row
        for i in range(self.board_y_size):

            # Compares each row with each subsequent row
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
        """ Checks whether columns are repeated
        :return boolean: True if no columns are repeated, False otherwise
        """

        # Loops through each column
        for i in range(self.board_x_size):

            # Compares each column with each subsequent column
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

    def change_click(self):
        self.switch_window.emit()

    def update_timer(self):
        """ Called at the predetermined rate to update the timer label regularly
        """

        if self.game_status == 1:  # Only update timer when game is being played
            n_secs = time.time() - self._timer_start_nsecs  # Finds the time passed since the game started
            self.clock.setText("Time: %07.3f" % n_secs)  # Updates the timer label to display time elapsed
        else:
            self._timer_start_nsecs += 0.01
