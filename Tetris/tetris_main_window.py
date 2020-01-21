# Tetris main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

import time
from enum import IntEnum

# PyQt5 specific imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from tetris_board import Status
from tetris_board import TetrisBoard
from tetris_tetromino_display_box import TetrominoDisplay


class Game_Mode(IntEnum):
    Sprint = 0
    Battle2p = 1
    Marathon = 2


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

        self.game_mode = Game_Mode.Battle2p

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
        vb_center = QVBoxLayout()
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

        self.stats_group_box = QGroupBox("Statistics")
        vb_stats = QVBoxLayout()
        f.setPointSize(10)
        f.setWeight(55)

        # Time label
        time_elapsed_box = QHBoxLayout()

        self.time_elapsed_text = QLabel()
        self.time_elapsed_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.time_elapsed_text.setFont(f)
        self.time_elapsed_text.setText("Time Elapsed: ")

        self.time_elapsed_label = QLabel()
        self.time_elapsed_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.time_elapsed_label.setFont(f)
        self.time_elapsed_label.setText("%07.3f" % 0)

        time_elapsed_box.addWidget(self.time_elapsed_text, 0, Qt.Alignment())
        time_elapsed_box.addWidget(self.time_elapsed_label, 0, Qt.Alignment())
        vb_stats.addLayout(time_elapsed_box)

        # Create combo label
        self.is_in_combo = False
        self.current_combo = -1
        current_combo_box = QHBoxLayout()

        self.combo_number_text = QLabel()
        self.combo_number_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.combo_number_text.setFont(f)
        self.combo_number_text.setText("Combo number: ")

        self.combo_number_label = QLabel()
        self.combo_number_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.combo_number_label.setFont(f)
        self.combo_number_label.setText("%d" % max(0, self.current_combo))

        current_combo_box.addWidget(self.combo_number_text, 0, Qt.Alignment())
        current_combo_box.addWidget(self.combo_number_label, 0, Qt.Alignment())
        vb_stats.addLayout(current_combo_box)

        # Create max combo label
        self.max_combo = 0
        max_combo_box = QHBoxLayout()

        self.max_combo_text = QLabel()
        self.max_combo_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.max_combo_text.setFont(f)
        self.max_combo_text.setText("Max combo: ")

        self.max_combo_label = QLabel()
        self.max_combo_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.max_combo_label.setFont(f)
        self.max_combo_label.setText("%d" % self.max_combo)

        max_combo_box.addWidget(self.max_combo_text, 0, Qt.Alignment())
        max_combo_box.addWidget(self.max_combo_label, 0, Qt.Alignment())
        vb_stats.addLayout(max_combo_box)

        # Create number of tetrises label
        self.num_tetrises = 0
        num_tetrises_box = QHBoxLayout()

        self.num_tetrises_text = QLabel()
        self.num_tetrises_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.num_tetrises_text.setFont(f)
        self.num_tetrises_text.setText("Number of tetrises: ")

        self.num_tetrises_label = QLabel()
        self.num_tetrises_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.num_tetrises_label.setFont(f)
        self.num_tetrises_label.setText("%d" % self.num_tetrises)

        num_tetrises_box.addWidget(self.num_tetrises_text, 0, Qt.Alignment())
        num_tetrises_box.addWidget(self.num_tetrises_label, 0, Qt.Alignment())
        vb_stats.addLayout(num_tetrises_box)

        # Create number of pieces placed label
        self.num_pieces_placed = 0
        num_pieces_box = QHBoxLayout()

        self.num_pieces_text = QLabel()
        self.num_pieces_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.num_pieces_text.setFont(f)
        self.num_pieces_text.setText("Number of pieces: ")

        self.num_pieces_label = QLabel()
        self.num_pieces_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.num_pieces_label.setFont(f)
        self.num_pieces_label.setText("%d" % self.num_pieces_placed)

        num_pieces_box.addWidget(self.num_pieces_text, 0, Qt.Alignment())
        num_pieces_box.addWidget(self.num_pieces_label, 0, Qt.Alignment())
        vb_stats.addLayout(num_pieces_box)

        # Create lines cleared label
        self.lines_cleared = 0
        lines_cleared_box = QHBoxLayout()

        self.lines_cleared_text = QLabel()
        self.lines_cleared_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.lines_cleared_text.setFont(f)
        self.lines_cleared_text.setText("Lines cleared: ")

        self.lines_cleared_label = QLabel()
        self.lines_cleared_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.lines_cleared_label.setFont(f)
        self.lines_cleared_label.setText("%d" % self.lines_cleared)

        lines_cleared_box.addWidget(self.lines_cleared_text, 0, Qt.Alignment())
        lines_cleared_box.addWidget(self.lines_cleared_label, 0, Qt.Alignment())
        vb_stats.addLayout(lines_cleared_box)

        # Create lines sent label
        self.lines_sent = 0
        lines_sent_box = QHBoxLayout()

        self.lines_sent_text = QLabel()
        self.lines_sent_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.lines_sent_text.setFont(f)
        self.lines_sent_text.setText("Lines Sent: ")

        self.lines_sent_label = QLabel()
        self.lines_sent_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.lines_sent_label.setFont(f)
        self.lines_sent_label.setText("%d" % self.lines_sent)

        lines_sent_box.addWidget(self.lines_sent_text, 0, Qt.Alignment())
        lines_sent_box.addWidget(self.lines_sent_label, 0, Qt.Alignment())
        vb_stats.addLayout(lines_sent_box)

        # Create num actions label
        self.actions_done = 0
        actions_done_box = QHBoxLayout()

        self.actions_done_text = QLabel()
        self.actions_done_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.actions_done_text.setFont(f)
        self.actions_done_text.setText("Keys Pressed: ")

        self.actions_done_label = QLabel()
        self.actions_done_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.actions_done_label.setFont(f)
        self.actions_done_label.setText("%d" % self.actions_done)

        actions_done_box.addWidget(self.actions_done_text, 0, Qt.Alignment())
        actions_done_box.addWidget(self.actions_done_label, 0, Qt.Alignment())
        vb_stats.addLayout(actions_done_box)

        self.stats_group_box.setLayout(vb_stats)
        vb_right.addWidget(self.stats_group_box)

        # Create the board
        self.game_board = TetrisBoard()
        self.game_board.changed_game_status.connect(self.update_status_label)
        self.game_board.shifted_tetromino.connect(self.update_shift_piece)
        self.game_board.next_tetromino_update.connect(self.update_next_pieces)
        self.game_board.lines_cleared.connect(self.update_lines_cleared)
        self.game_board.new_game_started.connect(self.new_game_started)
        self.game_board.key_press.connect(self.key_pressed)
        vb_center.addWidget(self.game_board)

        # Create windows to display next pieces
        self.next_piece_display_1 = TetrominoDisplay()
        self.next_piece_display_2 = TetrominoDisplay()
        self.next_piece_display_3 = TetrominoDisplay()
        self.next_piece_display_4 = TetrominoDisplay()
        vb_next.addWidget(self.next_piece_display_1, 1, Qt.Alignment())
        vb_next.addWidget(self.next_piece_display_2, 1, Qt.Alignment())
        vb_next.addWidget(self.next_piece_display_3, 1, Qt.Alignment())
        vb_next.addWidget(self.next_piece_display_4, 3, Qt.Alignment())

        # Create a window to display the shifted piece
        self.shift_piece_display = TetrominoDisplay()
        vb_left.addWidget(self.shift_piece_display, 1, Qt.Alignment())

        self.main_information = QLabel()
        self.main_information.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        f.setPointSize(20)
        f.setWeight(85)
        self.main_information.setFont(f)
        self.main_information.setText("0")
        vb_left.addWidget(self.main_information, 3, Qt.AlignTop)

        hb.addLayout(vb_left, 1)
        hb.addLayout(vb_center, 2)
        hb.addLayout(vb_next, 1)
        hb.addLayout(vb_right, 2)

        self.window.setLayout(hb)
        self.setCentralWidget(self.window)
        self.show()

    def update_status_label(self, new_game_state):
        if new_game_state != Status.NOT_BEGUN:
            self.game_state_label.setText(new_game_state.name)
        else:
            self.game_state_label.setText("PLAYING")

        self.current_game_state = new_game_state

    def new_game_started(self):
        self._timer_start_nsecs = time.time()

        self.lines_sent = 0
        self.lines_sent_label.setText("%d" % self.lines_sent)
        self.lines_cleared = 0
        self.lines_cleared_label.setText("%d" % self.lines_cleared)
        self.current_combo = -1
        self.combo_number_label.setText("%d" % max(0, self.current_combo))
        self.max_combo = 0
        self.max_combo_label.setText("%d" % self.max_combo)
        self.num_tetrises = 0
        self.num_tetrises_label.setText("%d" % self.num_tetrises)
        self.num_pieces_placed = 0
        self.num_pieces_label.setText("%d" % self.num_pieces_placed)
        self.actions_done = 0
        self.actions_done_label.setText("%d" % self.actions_done)

    def update_shift_piece(self, piece):
        self.shift_piece_display.update_identity(piece)

    def update_next_pieces(self, next_pieces):
        self.next_piece_display_1.update_identity(next_pieces[0])
        self.next_piece_display_2.update_identity(next_pieces[1])
        self.next_piece_display_3.update_identity(next_pieces[2])
        self.next_piece_display_4.update_identity(next_pieces[3])

    def update_lines_cleared(self, lines):
        self.lines_cleared += lines
        self.lines_cleared_label.setText("%d" % self.lines_cleared)

        self.current_combo = self.current_combo + 1 if lines > 0 else -1
        self.combo_number_label.setText("%d" % max(0, self.current_combo))

        if self.current_combo > self.max_combo:
            self.max_combo = self.current_combo
            self.max_combo_label.setText("%d" % self.max_combo)

        self.num_pieces_placed += 1
        self.num_pieces_label.setText("%d" % self.num_pieces_placed)

        self.lines_sent += TetrisMainWindow.simple_lines_table[lines]
        self.lines_sent += TetrisMainWindow.combo_table_facebook[max(0, self.current_combo)]
        self.lines_sent_label.setText("%d" % self.lines_sent)

        if lines == 4:
            self.num_tetrises += 1
            self.num_tetrises_label.setText("%d" % self.num_tetrises)

        if self.game_mode == Game_Mode.Sprint:
            if self.lines_cleared > 39:
                self.game_board.end_game()

    def game_started(self):
        self._timer.start(10)

    def update_timer(self):
        if self.current_game_state == Status.PLAYING:
            n_secs = time.time() - self._timer_start_nsecs  # Finds the time passed since the game started
            self.time_elapsed_label.setText("%07.3f" % n_secs)
            if self.game_mode == Game_Mode.Battle2p and n_secs > 120:
                self.game_board.end_game()
        else:
            self._timer_start_nsecs += 0.01  # If not playing, we increment the timer (i.e. hints)

    def key_pressed(self):
        self.actions_done += 1
        self.actions_done_label.setText("%d" % self.actions_done)
