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
from .minesweeper_cell_v1 import Cell


class MainWindow(QMainWindow):
    """ Main window for the minesweeper interface
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Minesweeper'
        self.board_x_size = 30
        self.board_y_size = 16
        self.num_mines = 99
        self.mines_left = self.num_mines
        self.setWindowTitle(self.title)
        self.first_already_clicked = False
        self.num_cells_clicked = 0
        self.game_status = 0
        self._timer_start_nsecs = 0

        w = QWidget()
        vb = QVBoxLayout()

        hb = QHBoxLayout()

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.pressed.connect(self.button_click)
        hb.addWidget(self.reset_button, 0, Qt.Alignment())

        self.status = QLabel()
        self.status.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.status.font()
        f.setPointSize(20)
        f.setWeight(75)
        self.status.setFont(f)
        self.status.setText("000")
        hb.addWidget(self.status, 0, Qt.Alignment())

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.mines.setFont(f)
        self.mines.setText("%03d" % self.num_mines)
        hb.addWidget(self.mines, 0, Qt.Alignment())

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.clock.setFont(f)
        self.clock.setText("Time: 000.000")
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(10)  # 1 second timer
        hb.addWidget(self.clock, 0, Qt.Alignment())

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
                        if w.is_mine:
                            self.game_over()

    def game_over(self):
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_revealed = True
                w.update()
        self.status.setText("Failed!")
        self.game_status = 0

    def button_click(self):

        self.first_already_clicked = False

        # Clear all mine positions
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset_cell()

        self.set_up_map()
        self.mines_left = self.num_mines
        self.status.setText("000")
        self.mines.setText("%03d" % self.mines_left)
        self.clock.setText("Time: 000.000")
        self.game_status = 0

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
            self.game_status = 1
            self._timer_start_nsecs = int(time.time())

        num_clicked = 0
        for x in range(0, self.board_x_size):
            for y in range(0, self.board_y_size):
                w = self.grid.itemAtPosition(y, x).widget()
                if w.is_revealed:
                    num_clicked = num_clicked + 1
        if num_clicked == self.board_x_size * self.board_y_size - self.num_mines:
            self.status.setText("Hooray!")
            self.game_status = 0

    def cell_flagged(self, add):
        self.mines_left = self.mines_left - add
        self.mines.setText("%03d" % self.mines_left)

    def update_timer(self):
        if self.game_status == 1:
            n_secs = time.time() - self._timer_start_nsecs
            self.clock.setText("Time: %07.3f" % n_secs)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
