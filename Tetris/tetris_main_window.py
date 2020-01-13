# Tetris main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

import time

# PyQt5 specific imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from tetris_board import Status
from tetris_board import TetrisBoard
from tetris_tetromino_display_box import TetrominoDisplay


class TetrisMainWindow(QMainWindow):
    """ Main class window for the binairo game
    """

    # Signal when the button to edit board size and difficulty is pressed
    switch_window = pyqtSignal()

    simple_lines_table = [0, 0, 1, 2, 4]
    combo_table_jstris = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5]
    combo_table_facebook = [0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Tetris'  # Name of the window to be opened
        self.setWindowTitle(self.title)  # Sets the name of the window to be the title

        self.width = 10
        self.height = 20
        self.resize(980, 630)

        # Create a timer to keep track of the game
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)  # Connects the timer to self.update_timer
        self._timer.start(10)                           # Updates and calls self.update_timer every 10 ms
        self._timer_start_nsecs = 0

        self.window = QWidget(*args, **kwargs)
        vb_left = QVBoxLayout()
        vb_right = QVBoxLayout()
        vb_next = QVBoxLayout()
        hb = QHBoxLayout()

        # Create the game status label
        self.current_game_state = None
        self.game_state_label = QLabel()
        self.game_state_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.game_state_label.font()  # Sets the font
        f.setPointSize(10)
        f.setWeight(75)
        self.game_state_label.setFont(f)
        self.game_state_label.setText("Press Enter to Start")
        vb_right.addWidget(self.game_state_label, 0, Qt.Alignment())

        # Time label
        self.time_elapsed_label = QLabel()
        self.time_elapsed_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.time_elapsed_label.setFont(f)
        self.time_elapsed_label.setText("Time: %07.3f" % 0)
        vb_right.addWidget(self.time_elapsed_label, 0, Qt.Alignment())

        # Create lines cleared label
        self.lines_cleared = 0
        self.lines_cleared_label = QLabel()
        self.lines_cleared_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lines_cleared_label.setFont(f)
        self.lines_cleared_label.setText("Lines cleared: %d" % self.lines_cleared)
        vb_right.addWidget(self.lines_cleared_label, 0, Qt.Alignment())

        # Create combo label
        self.is_in_combo = False
        self.current_combo = -1
        self.combo_number_label = QLabel()
        self.combo_number_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.combo_number_label.setFont(f)
        self.combo_number_label.setText("Combo number: %d" % max(0, self.current_combo))
        vb_right.addWidget(self.combo_number_label, 0, Qt.Alignment())

        # Create lines sent label
        self.lines_sent = 0
        self.lines_sent_label = QLabel()
        self.lines_sent_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lines_sent_label.setFont(f)
        self.lines_sent_label.setText("Lines Sent: %d" % self.lines_sent)
        vb_right.addWidget(self.lines_sent_label, 0, Qt.Alignment())

        # Create the board
        self.game_board = TetrisBoard()
        self.game_board.changed_game_status.connect(self.update_status_label)
        self.game_board.shifted_tetromino.connect(self.update_shift_piece)
        self.game_board.next_tetromino_update.connect(self.update_next_pieces)
        self.game_board.lines_cleared.connect(self.update_lines_cleared)
        self.game_board.new_game_started.connect(self.new_game_started)
        vb_left.addWidget(self.game_board)

        # Create a window to display the shifted piece
        self.shift_piece_display = TetrominoDisplay()
        hb.addWidget(self.shift_piece_display, 1, Qt.Alignment())

        # Create windows to display next pieces
        self.next_piece_display_1 = TetrominoDisplay()
        self.next_piece_display_2 = TetrominoDisplay()
        self.next_piece_display_3 = TetrominoDisplay()
        self.next_piece_display_4 = TetrominoDisplay()
        vb_next.addWidget(self.next_piece_display_1, 1, Qt.Alignment())
        vb_next.addWidget(self.next_piece_display_2, 1, Qt.Alignment())
        vb_next.addWidget(self.next_piece_display_3, 1, Qt.Alignment())
        vb_next.addWidget(self.next_piece_display_4, 3, Qt.Alignment())

        hb.addLayout(vb_left, 2)
        hb.addLayout(vb_next, 1)
        hb.addLayout(vb_right, 2)

        self.window.setLayout(hb)
        self.setCentralWidget(self.window)
        self.show()

    def update_status_label(self, new_game_state):
        self.game_state_label.setText(new_game_state.name)
        self.current_game_state = new_game_state

    def new_game_started(self):
        self._timer_start_nsecs = time.time()

    def update_shift_piece(self, piece):
        self.shift_piece_display.update_identity(piece)

    def update_next_pieces(self, next_pieces):
        self.next_piece_display_1.update_identity(next_pieces[0])
        self.next_piece_display_2.update_identity(next_pieces[1])
        self.next_piece_display_3.update_identity(next_pieces[2])
        self.next_piece_display_4.update_identity(next_pieces[3])

    def update_lines_cleared(self, lines):
        self.lines_cleared += lines
        self.lines_cleared_label.setText("Lines cleared: %d" % self.lines_cleared)

        self.current_combo = self.current_combo + 1 if lines > 0 else -1
        self.combo_number_label.setText("Current combo: %d" % max(0, self.current_combo))

        self.lines_sent += TetrisMainWindow.simple_lines_table[lines]
        self.lines_sent += TetrisMainWindow.combo_table_facebook[max(0, self.current_combo)]
        self.lines_sent_label.setText("Lines sent: %d" % self.lines_sent)

    def game_started(self):
        self._timer.start(10)

    def update_timer(self):
        if self.current_game_state == Status.PLAYING:
            n_secs = time.time() - self._timer_start_nsecs  # Finds the time passed since the game started
            self.time_elapsed_label.setText("Time: %07.3f" % n_secs)
        else:
            self._timer_start_nsecs += 0.01  # If not playing, we increment the timer (i.e. hints)


