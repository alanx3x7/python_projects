# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from enum import IntEnum
import numpy as np
import time
import random

from tetris_tetromino import Tetromino
from tetris_enums import Direction
from tetris_enums import Shape


class Status(IntEnum):
    PAUSED = 0
    PLAYING = 1
    GAMEOVER = 2
    NOT_BEGUN = 3


class TetrisBoard(QWidget):

    changed_game_status = pyqtSignal(Status)
    shifted_tetromino = pyqtSignal(Shape)
    next_tetromino_update = pyqtSignal(list)
    lines_cleared = pyqtSignal(int)
    new_game_started = pyqtSignal()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.width = 10
        self.height = 20

        self.speed = 1000
        self.cell_side_length = 30
        self.start_pos = (4, 0)
        self.colour_table = [0x000000, 0xFF0000, 0x00FF00, 0x00FFFF, 0x800080, 0xFFFF00, 0xFFA500, 0x0000FF]

        self.game_status = Status.NOT_BEGUN
        self.display_text = None

        # Key press things
        self.up_key_last_released = False
        self.up_key_start = time.time()

        self.x_cell_corners = np.zeros(self.width)
        for x in range(self.width):
            self.x_cell_corners[x] = x * self.cell_side_length + 5

        self.y_cell_corners = np.zeros(self.height)
        for y in range(self.height):
            self.y_cell_corners[y] = y * self.cell_side_length + 5

        self.board = np.zeros((self.height, self.width))

        self.gravity_timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

        self.soft_drop_timer_L1 = QBasicTimer()
        self.soft_drop_timer_L2 = QBasicTimer()
        self.soft_drop_timer_L3 = QBasicTimer()
        self.L1 = 500
        self.L2 = 5000
        self.L3 = 20000

        self.floating = None
        self.ghost = None
        self.num_next_pieces = 4
        self.next_pieces = [Shape.NoShape] * self.num_next_pieces
        self.shifted = None
        self.shifted_this_piece = False

        # DAS and ARR Control
        self.das_speed = 133
        self.arr_speed = 20

        self.was_interrupted = False

        # Left key move timers
        self.left_move_arr_timer = QBasicTimer()
        self.left_move_das_timer = QBasicTimer()
        self.left_key_enter_das = False
        self.left_key_enter_arr = False

        # Right key move timers
        self.right_move_arr_timer = QBasicTimer()
        self.right_move_das_timer = QBasicTimer()
        self.right_key_enter_das = False
        self.right_key_enter_arr = False

        QApplication.processEvents()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.paintFixed(p)

        if self.display_text is not None:
            self.paintText(p, event)

        if self.ghost is not None:
            self.paintGhost(p)

        if self.floating is not None:
            self.paintFloat(p)

    def paintFixed(self, p):

        outer = Qt.white
        inner = Qt.black

        p.setPen(QPen(outer, 0.5, Qt.SolidLine))
        p.setBrush(QBrush(inner, Qt.SolidPattern))

        for y in range(self.height):
            for x in range(self.width):
                inner = Qt.black if self.board[y, x] == 0 else QColor(self.colour_table[int(self.board[y, x])])
                p.setBrush(QBrush(inner, Qt.SolidPattern))
                p.drawRect(self.x_cell_corners[x], self.y_cell_corners[y], 30, 30)

    def paintText(self, p, event):
        p.setPen(QPen(Qt.gray, 0, Qt.SolidLine))
        p.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        p.drawRect(5, 260, self.size().width() - 9, 80)

        p.setPen(QColor(255, 0, 0))
        p.setFont(QFont('Decorative', 30))
        p.drawText(event.rect(), Qt.AlignCenter, self.display_text)

    def paintFloat(self, p):

        outer = Qt.white
        inner = QColor(self.colour_table[self.floating.identity.value])

        p.setPen(QPen(outer, 2, Qt.SolidLine))
        p.setBrush(QBrush(inner, Qt.SolidPattern))

        for positions in self.floating.coordinates:
            if positions[0] > -1 and positions[1] > -1:
                p.drawRect(self.x_cell_corners[positions[0]], self.y_cell_corners[positions[1]], 30, 30)

    def paintGhost(self, p):

        outer = Qt.white
        inner = Qt.darkGray

        p.setPen(QPen(outer, 2, Qt.SolidLine))
        p.setBrush(QBrush(inner, Qt.SolidPattern))

        for positions in self.ghost:
            if positions[0] > -1 and positions[1] > -1:
                p.drawRect(self.x_cell_corners[positions[0]], self.y_cell_corners[positions[1]], 30, 30)

    def start_game(self):

        self.game_status = Status.NOT_BEGUN
        self.changed_game_status.emit(self.game_status)
        self.gravity_timer.stop()
        self.board = np.zeros((self.height, self.width))
        self.floating = None
        self.shifted = None
        self.shifted_this_piece = False
        self.shifted_tetromino.emit(Shape.NoShape)
        self.update_ghost()
        self.next_pieces = [Shape.NoShape] * self.num_next_pieces
        self.next_tetromino_update.emit(self.next_pieces)

        self.display_text = "Ready?"
        self.update()

        QTimer().singleShot(1000, self.start_stage_1)

    def start_stage_1(self):
        self.display_text = "Go!"
        self.update()

        QTimer().singleShot(1000, self.start_stage_2)

    def start_stage_2(self):
        self.display_text = None
        self.update()

        for i in range(self.num_next_pieces):
            self.next_pieces[i] = Shape(random.randint(1, 7))
        self.next_tetromino_update.emit(self.next_pieces)

        self.floating = Tetromino(self.start_pos)
        self.soft_drop_timer_L3.start(self.L3, Qt.PreciseTimer, self)
        self.update_ghost()
        self.game_status = Status.PLAYING
        self.changed_game_status.emit(self.game_status)
        self.new_game_started.emit()
        self.gravity_timer.start(self.speed, self)

    def resume_game(self):
        self.game_status = Status.PLAYING
        self.changed_game_status.emit(self.game_status)
        self.gravity_timer.start(self.speed, self)

    def pause_game(self):
        self.game_status = Status.PAUSED
        self.changed_game_status.emit(self.game_status)
        self.gravity_timer.stop()

    def end_game(self):
        self.game_status = Status.GAMEOVER
        self.soft_drop_timer_L1.stop()
        self.soft_drop_timer_L2.stop()
        self.soft_drop_timer_L3.stop()
        self.changed_game_status.emit(self.game_status)
        self.gravity_timer.stop()

    def timerEvent(self, event):

        if event.timerId() == self.left_move_arr_timer.timerId():
            self.move_floating_piece(-1, 0)
            self.update()

        elif event.timerId() == self.right_move_arr_timer.timerId():
            self.move_floating_piece(1, 0)
            self.update()

        elif event.timerId() == self.left_move_das_timer.timerId():
            if self.left_key_enter_das:
                self.left_move_arr_timer.start(self.arr_speed, Qt.PreciseTimer, self)
                self.left_move_das_timer.stop()
                self.left_key_enter_das = False
                self.left_key_enter_arr = True
                self.move_floating_piece(-1, 0)
                self.update()

        elif event.timerId() == self.right_move_das_timer.timerId():
            if self.right_key_enter_das:
                self.right_move_arr_timer.start(self.arr_speed, Qt.PreciseTimer, self)
                self.right_move_das_timer.stop()
                self.right_key_enter_das = False
                self.right_key_enter_arr = True
                self.move_floating_piece(1, 0)
                self.update()

        elif event.timerId() == self.gravity_timer.timerId():
            if not self.soft_drop_timer_L1.isActive():
                self.gravity()

        elif event.timerId() == self.soft_drop_timer_L1.timerId():
            self.soft_drop_timer_L1.stop()
            self.soft_drop_timer_L2.stop()
            self.soft_drop_timer_L3.stop()
            self.drop_floating()

        elif event.timerId() == self.soft_drop_timer_L2.timerId():
            self.soft_drop_timer_L1.stop()
            self.soft_drop_timer_L2.stop()
            self.soft_drop_timer_L3.stop()
            self.drop_floating()

        elif event.timerId() == self.soft_drop_timer_L3.timerId():
            self.soft_drop_timer_L1.stop()
            self.soft_drop_timer_L2.stop()
            self.soft_drop_timer_L3.stop()
            self.drop_floating()

        else:
            super(TetrisBoard, self).timerEvent(event)

    def gravity(self):
        if self.move_floating_piece(0, 1):
            self.soft_drop_timer_L1.stop()
            self.soft_drop_timer_L2.stop()
            self.soft_drop_timer_L3.stop()
            self.update()
            return

        if not self.soft_drop_timer_L1.isActive():
            self.soft_drop_timer_L1.start(self.L1, Qt.PreciseTimer, self)

        if not self.soft_drop_timer_L2.isActive():
            self.soft_drop_timer_L2.start(self.L2, Qt.PreciseTimer, self)

    def drop_floating(self):
        while self.move_floating_piece(0, 1):
            does_nothing = 1
        self.fix_floating_piece()
        self.clear_full_rows()
        self.create_new_piece()
        self.shifted_this_piece = False

    def move_floating_piece(self, x, y, ghost_update=False):

        if self.try_move_floating(x, y):
            if not ghost_update:
                self.update_ghost()
            return True
        else:
            return False

    def is_touching_ground(self):
        for positions in self.floating.coordinates:
            if positions[1] + 1 >= self.height:
                return True
            elif self.board[positions[1] + 1, positions[0] + 1] != 0:
                return True
        return False

    def try_move_floating(self, x, y):

        new_positions = []
        for positions in self.floating.coordinates:
            new_x = positions[0] + x
            new_y = positions[1] + y

            if new_x >= self.width or new_x < 0 or new_y >= self.height:
                return False

            if new_y > -1 and self.board[new_y, new_x] != 0:
                return False

            new_positions.append([new_x, new_y])

        new_center = [self.floating.center[0] + x, self.floating.center[1] + y]
        self.floating.move_to(new_center, new_positions)

        return True

    def fix_floating_piece(self):

        for positions in self.floating.coordinates:
            if 0 <= positions[0] < self.width and 0 <= positions[1] < self.height:
                self.board[positions[1], positions[0]] = self.floating.identity.value

    def create_new_piece(self):
        self.floating = Tetromino(self.start_pos, self.next_pieces[0])
        for i in range(self.num_next_pieces):
            if i != self.num_next_pieces - 1:
                self.next_pieces[i] = self.next_pieces[i + 1]
            else:
                self.next_pieces[i] = Shape(random.randint(1, 7))
        self.next_tetromino_update.emit(self.next_pieces)

        for positions in self.floating.coordinates:
            if positions[0] > -1 and positions[1] > -1:
                if self.board[positions[1], positions[0]] != 0:
                    self.end_game()
                    return

        self.soft_drop_timer_L1.stop()
        self.soft_drop_timer_L2.stop()
        self.soft_drop_timer_L3.start(self.L3, Qt.PreciseTimer, self)
        self.update_ghost()
        self.update()

    def rotate_floating_piece(self, direction):
        if direction == Direction.RIGHT:
            self.floating.rotate_right()
        else:
            self.floating.rotate_left()

        is_valid = False
        for positions in self.floating.wall_kick_offset(direction):
            if self.try_move_floating(positions[0], positions[1]):
                is_valid = True
                break

        if is_valid:
            self.update_ghost()
        elif not is_valid and direction == Direction.RIGHT:
            self.floating.rotate_left()
        elif not is_valid and direction == Direction.LEFT:
            self.floating.rotate_right()

    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_F4:
            self.start_game()

        if self.game_status == Status.NOT_BEGUN and key == Qt.Key_Return:
            self.start_game()
        elif self.game_status == Status.GAMEOVER and key == Qt.Key_R:
            self.start_game()

        if key == Qt.Key_P:
            if self.game_status == Status.PAUSED:
                self.resume_game()
            elif self.game_status == Status.PLAYING:
                self.pause_game()

        if self.game_status == Status.NOT_BEGUN:
            super(TetrisBoard, self).keyPressEvent(event)
            return

        if self.game_status == Status.PAUSED or self.game_status == Status.GAMEOVER:
            super(TetrisBoard, self).keyPressEvent(event)
            return

        if key == Qt.Key_Left:
            if not event.isAutoRepeat():
                self.left_key_enter_das = True

                if self.right_key_enter_arr:
                    self.right_key_enter_das = True
                    self.right_key_enter_arr = False
                    self.right_move_arr_timer.stop()
                    self.right_move_das_timer.start(self.das_speed, Qt.PreciseTimer, self)

                self.left_move_das_timer.start(self.das_speed, self)

                if self.move_floating_piece(-1, 0):
                    if self.soft_drop_timer_L1.isActive():
                        if self.is_touching_ground():
                            self.soft_drop_timer_L1.start(self.L1, Qt.PreciseTimer, self)
                        else:
                            self.soft_drop_timer_L1.stop()
                            self.soft_drop_timer_L2.stop()
                self.update()

        elif key == Qt.Key_Right:
            if not event.isAutoRepeat():
                self.right_key_enter_das = True

                if self.left_key_enter_arr:
                    self.left_key_enter_das = True
                    self.left_key_enter_arr = False
                    self.left_move_arr_timer.stop()
                    self.left_move_das_timer.start(self.das_speed, Qt.PreciseTimer, self)

                self.right_move_das_timer.start(self.das_speed, self)

                if self.move_floating_piece(1, 0):
                    if self.soft_drop_timer_L1.isActive():
                        if self.is_touching_ground():
                            self.soft_drop_timer_L1.start(self.L1, Qt.PreciseTimer, self)
                        else:
                            self.soft_drop_timer_L1.stop()
                            self.soft_drop_timer_L2.stop()

        elif key == Qt.Key_Down:
            if not self.move_floating_piece(0, 1) and not self.soft_drop_timer_L1.isActive():
                self.soft_drop_timer_L1.start(self.L1, self)
                self.soft_drop_timer_L2.start(self.L2, self)

        elif key == Qt.Key_Up:
            if not event.isAutoRepeat():
                self.rotate_floating_piece(Direction.RIGHT)

        elif key == Qt.Key_Space:
            if not event.isAutoRepeat():
                self.drop_floating()

        elif key == Qt.Key_Shift:
            if not event.isAutoRepeat():
                self.handle_shift_key()

        elif key == Qt.Key_Q:
            self.end_game()

        self.update()

    def keyReleaseEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            if not event.isAutoRepeat():
                self.left_key_enter_das = False
                self.left_key_enter_arr = False
                self.left_move_arr_timer.stop()
                self.left_move_das_timer.stop()

        elif key == Qt.Key_Right:
            if not event.isAutoRepeat():
                self.right_key_enter_das = False
                self.right_key_enter_arr = False
                self.right_move_arr_timer.stop()
                self.right_move_das_timer.stop()

    def clear_full_rows(self):

        lines_to_clear = []
        for y in range(self.height):
            if np.count_nonzero(self.board[y, :]) == self.width:
                lines_to_clear.append(y)

        for line in lines_to_clear:
            for y in range(line - 1, -1, -1):
                self.board[y + 1, :] = self.board[y, :]
                self.board[0, :] = np.zeros(self.width)

        self.lines_cleared.emit(len(lines_to_clear))

    def handle_shift_key(self):

        if not self.shifted_this_piece:
            if self.shifted is None:
                self.shifted = self.floating.identity
                self.create_new_piece()
                self.shifted_this_piece = True
                self.shifted_tetromino.emit(self.shifted)
            else:
                temp_tetromino = self.shifted
                self.shifted = self.floating.identity
                self.floating = Tetromino(self.start_pos, temp_tetromino)
                self.shifted_this_piece = True
                self.shifted_tetromino.emit(self.shifted)
            self.soft_drop_timer_L1.stop()
            self.soft_drop_timer_L2.stop()
            self.soft_drop_timer_L3.start(self.L3, Qt.PreciseTimer, self)
            self.update_ghost()

    def update_ghost(self):

        if self.floating is None:
            self.ghost = None
            return

        current_center = self.floating.center
        while self.move_floating_piece(0, 1, True):
            does_nothing = 1
        self.ghost = self.floating.coordinates
        self.floating.update_center(current_center[0], current_center[1])
        self.floating.move_to_center()
