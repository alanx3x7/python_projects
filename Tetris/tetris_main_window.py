# Tetris main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

# Typical imports
import random
import time
import numpy as np

# PyQt5 specific imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from tetris_board import TetrisBoard
from tetris_tetromino_display_box import TetrominoDisplay

from tetris_board import Status


class TetrisMainWindow(QMainWindow):
    """ Main class window for the binairo game
    """

    # Signal when the button to edit board size and difficulty is pressed
    switch_window = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Tetris'  # Name of the window to be opened
        self.setWindowTitle(self.title)  # Sets the name of the window to be the title

        self.width = 10
        self.height = 20
        self.resize(850, 630)

        self.window = QWidget(*args, **kwargs)
        vb_left = QVBoxLayout()
        vb_right = QVBoxLayout()
        hb = QHBoxLayout()

        # Create the game status label
        self.game_state_label = QLabel()
        self.game_state_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.game_state_label.font()  # Sets the font
        f.setPointSize(10)
        f.setWeight(75)
        self.game_state_label.setFont(f)
        self.game_state_label.setText("Press Enter to Start")
        vb_right.addWidget(self.game_state_label, 0, Qt.Alignment())

        # Create shift piece label (temporary)
        self.shift_piece_label = QLabel()
        self.shift_piece_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.shift_piece_label.setFont(f)
        self.shift_piece_label.setText("None")
        vb_right.addWidget(self.shift_piece_label, 0, Qt.Alignment())

        # Create a window to display the shifted piece
        self.shift_piece_display = TetrominoDisplay()

        # Create the board
        self.game_board = TetrisBoard()
        self.game_board.changed_game_status.connect(self.update_status_label)
        self.game_board.shifted_tetromino.connect(self.update_shift_piece)
        vb_left.addWidget(self.game_board)

        hb.addWidget(self.shift_piece_display, 1, Qt.Alignment())
        hb.addLayout(vb_left, 2)
        hb.addLayout(vb_right, 2)

        self.window.setLayout(hb)
        self.setCentralWidget(self.window)
        self.show()

    def update_status_label(self, new_game_state):
        self.game_state_label.setText(new_game_state.name)

    def update_shift_piece(self, piece):
        self.shift_piece_label.setText(piece.name)
        self.shift_piece_display.update_identity(piece)
