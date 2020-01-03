# Minesweeper main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/02

# Typical imports
import sys
import random
import time

# PyQt5 specific imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Importing the class file for the individual cells
from minesweeper_cell_v1 import Cell


class MainWindow(QMainWindow):
    """ Main window for the minesweeper interface
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Minesweeper'      # Name of the window to be opened
        self.setWindowTitle(self.title)         # Sets the name of the window to be the title

        self.board_x_size = 30                  # Initializes the x size of the board (width)
        self.board_y_size = 16                  # Initializes the y size of the board (height)
        self.num_mines = 99                     # Initializes the number of mines on the board

        self.mines_left = self.num_mines        # Keeps track of number of mines left unflagged on board
        self.first_already_clicked = False      # Checks whether the first move has been made or not
        self.game_status = 0                    # Tracks status of game (1 = playing, 0 = otherwise)
        self._timer_start_nsecs = 0             # Initializes timer to 0

        # Creates a widget object, a vertical box object, and a horizontal box object
        w = QWidget()
        vb = QVBoxLayout()
        hb = QHBoxLayout()

        # Creates the reset button
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.pressed.connect(self.button_click)    # Links the click to self.button_click function
        hb.addWidget(self.reset_button, 0, Qt.Alignment())      # Adds the button to the horizontal box

        # Creates the status label
        self.status = QLabel()
        self.status.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.status.font()                                  # Sets the font
        f.setPointSize(20)
        f.setWeight(75)
        self.status.setFont(f)
        self.status.setText("000")
        hb.addWidget(self.status, 0, Qt.Alignment())            # Adds the status label to the horizontal box

        # Creates the mines label (number of mines remaining unflagged)
        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.mines.setFont(f)
        self.mines.setText("%03d" % self.num_mines)
        hb.addWidget(self.mines, 0, Qt.Alignment())             # Adds the mines label to the horizontal box

        # Create the clock label (timer)
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.clock.setFont(f)
        self.clock.setText("Time: 000.000")
        hb.addWidget(self.clock, 0, Qt.Alignment())             # Adds the clock label to the horizontal box

        # Create the timer object to keep track of time
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)          # Connects the timer to self.update_timer
        self._timer.start(10)  # 1 second timer                 # Updates and calls self.update_timer every 10 ms

        # Adds the horizontal box to the vertical box
        vb.addLayout(hb)

        # Create a grid layout to hold all of the cell objects for each cell
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        vb.addLayout(self.grid)                                 # Adds the grid to the vertical box

        # Sets the layout of the widget to be the vertical box and centers it
        w.setLayout(vb)
        self.setCentralWidget(w)

        # Initializes grid with cell objects and sets up the minefield
        self.init_map()
        self.set_up_map()

        # Displays the window
        self.show()

    def init_map(self):
        """ Initializes the grid object to hold a cell object at each position
        """

        # Loops through all positions of the grid
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):

                # Creates a cell object and add it to the grid at position (y, x)
                w = Cell(x, y)
                self.grid.addWidget(w, y, x)

                # Connect the signals for each cell to the respective functions
                w.clicked.connect(self.cell_clicked)                # Called when cell is clicked
                w.expandable.connect(self.expand_reveal)            # Called when cell without adjacencies is clicked
                w.oh_no.connect(self.game_over)                     # Called when cell with mine is clicked
                w.double_clicked.connect(self.expand_dc_reveal)     # Called when cell is double-clicked
                w.flagged.connect(self.cell_flagged)                # Called when cell is flagged

    def set_up_map(self):
        """ Initializes the mine positions in the grid that is set up
        """

        # Temporary container to contain the positions of the mines in the board
        positions = []

        # Places mines until there are num_mines mines in the minefield
        while len(positions) < self.num_mines:

            # Randomizes the location, making sure that the same location is not picked twice
            x = random.randint(0, self.board_x_size - 1)
            y = random.randint(0, self.board_y_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                positions.append((x, y))

        # Loops through all cells and calculates the adjacencies for each cell
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.num_adjacent = self.get_adjacency_n(x, y)

    def get_adjacency_n(self, x, y):
        """ Calculates the number of adjacent cells that are mines to the current cell
        :param x: The x coordinate of the current cell
        :param y: The y coordinate of the current cell
        :return n_mines: The number of adjacent cells that are mines to the current cell
        """

        positions = self.get_surrounding(x, y)                      # Get coordinate of the cells surrounding this cell
        n_mines = sum(1 if w.is_mine else 0 for w in positions)     # Finds the number of mines around this cell
        return n_mines

    def get_surrounding(self, x, y):
        """ Finds the coordinates of the cells adjacent to this cell on the minefield
        :param x: The x coordinate of the current cell
        :param y: The y coordinate of the current cell
        :return positions: The coordinates of the adjacent cells
        """

        positions = []
        for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())

        return positions

    def update_timer(self):
        """ Called at the predetermined rate to update the timer label regularly
        """

        if self.game_status == 1:                               # Only update timer when game is being played
            n_secs = time.time() - self._timer_start_nsecs      # Finds the time passed since the game started
            self.clock.setText("Time: %07.3f" % n_secs)         # Updates the timer label to display time elapsed

    def button_click(self):
        """ Called when the button is clicked - minefield and timer are reset
        """

        self.first_already_clicked = False                      # Makes sure that the first mine clicked is not true

        # Clear all mine positions by resetting each cell
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset_cell()

        self.set_up_map()                                       # Sets up the minefield again
        self.mines_left = self.num_mines                        # Resets the number of flagged mines
        self.status.setText("000")                              # Resets the status label
        self.mines.setText("%03d" % self.mines_left)            # Resets the mines remaining label
        self.clock.setText("Time: 000.000")                     # Resets the timer label
        self.game_status = 0                                    # Sets game status to 0

    def cell_clicked(self, x, y):
        """ Called when a cell is clicked and a signal is emitted
        :param x: The x coordinate of the current cell
        :param y: The y coordinate of the current cell
        """

        # If this is the first cell that is clicked in a new game
        if not self.first_already_clicked:
            t = self.grid.itemAtPosition(y, x).widget()

            # Continues to reset the minefield until the current cell has no adjacent mines
            while t.num_adjacent != 0:
                self.button_click()
                t = self.grid.itemAtPosition(y, x).widget()

            self._timer_start_nsecs = int(time.time())          # Sets the game start time as now
            self.first_already_clicked = True                   # Marks the fact that the first click has occurred
            self.game_status = 1                                # Sets game status to playing
            t.click()                                           # Clicks on the current cell

        # Counts the number of cells that are revealed in the minefield
        num_clicked = 0
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                if w.is_revealed:
                    num_clicked = num_clicked + 1

        # Checks if the number of cells clicked is the number of non-mine cells
        if num_clicked == self.board_x_size * self.board_y_size - self.num_mines:
            self.status.setText("Hooray!")                      # If so, then the user wins
            self.game_status = 0                                # Updates game status to not playing

    def cell_flagged(self, add):
        """ Called when a cell is flagged or unflagged
        :param add: 1 if the cell is flagged, -1 if the cell is unflagged by user
        """

        self.mines_left = self.mines_left - add                 # Updates number of remaining mines unflagged
        self.mines.setText("%03d" % self.mines_left)            # Displays the update

    def expand_reveal(self, x, y):
        """ Called when an expand signal is received; reveals position around the current cell if they are not mines
        :param x: The x coordinate of the cell from which we should expand from
        :param y: The y coordinate of the cell from which we should expand from
        """

        # Looks at the neighbouring cells, and clicks on the cell if they are not mines, revealing them
        for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine:
                    w.click()

    def expand_dc_reveal(self, x, y):
        """ Called when the left and right mouse buttons are simultaneously clicked on a revealed cell
            This reveals the adjacent cells if the number of neighbouring cells that are flagged matches the number of
            adjacencies of the current cell
        :param x: The x coordinate of the cell that is double clicked
        :param y: The y coordinate of the cell that is double clicked
        """

        t = self.grid.itemAtPosition(y, x).widget()
        flags_adjacent = 0

        # Looks through all neighbours and counts the number of flags
        for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if w.is_flagged:
                    flags_adjacent = flags_adjacent + 1

        # If the number of flags is equivalent to the number of adjacencies
        if flags_adjacent == t.num_adjacent:
            for xi in range(max(0, x - 1), min(x + 2, self.board_x_size)):
                for yi in range(max(0, y - 1), min(y + 2, self.board_y_size)):
                    w = self.grid.itemAtPosition(yi, xi).widget()

                    # If the neighbouring cell is not flagged, we reveal it
                    if not w.is_flagged:
                        w.reveal()

                        # If it is a mine, it's game over
                        if w.is_mine:
                            self.game_over()

    def game_over(self):
        """ Called when a mine is clicked - the game ends
        """

        # Reveals all cells in the minefield
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_revealed = True
                w.update()

        # Updates the status label and the game status (to stop the clock)
        self.status.setText("Failed!")
        self.game_status = 0


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
