# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from enum import IntEnum
import numpy as np
import time

from tetris_tetromino import Tetromino
from tetris_enums import Direction


class Status(IntEnum):
    PAUSED = 0
    PLAYING = 1
    GAMEOVER = 2
    NOT_BEGUN = 3


class TetrisBoard(QWidget):

    changed_game_status = pyqtSignal(Status)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.width = 10
        self.height = 20
        self.speed = 1000
        self.cell_side_length = 30
        self.start_pos = (4, 0)
        self.colour_table = [0x000000, 0xFF0000, 0x00FF00, 0x00FFFF, 0x800080, 0xFFFF00, 0xFFA500, 0x0000FF]

        self.game_status = Status.NOT_BEGUN

        # Key press things
        self.up_key_last_released = False
        self.up_key_start = time.time()

        self.x_cell_corners = np.zeros(10)
        for x in range(self.width):
            self.x_cell_corners[x] = x * self.cell_side_length + 5

        self.y_cell_corners = np.zeros(20)
        for y in range(self.height):
            self.y_cell_corners[y] = y * self.cell_side_length + 5

        self.board = np.zeros((self.height, self.width))

        self.frame_timer = QBasicTimer()

        self.floating = None
        self.setFocusPolicy(Qt.StrongFocus)

        self.soft_drop_timer = QBasicTimer()
        self.soft_drop_timer_speed = 500

        # DAS and ARR Control
        self.das_speed = 200
        self.arr_speed = 20

        # Left key move timers
        self.left_move_arr_timer = QBasicTimer()
        self.left_move_das_timer = QBasicTimer()
        self.left_key_enter_das = False

        # Right key move timers
        self.right_move_arr_timer = QBasicTimer()
        self.right_move_das_timer = QBasicTimer()
        self.right_key_enter_das = False

        QApplication.processEvents()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.paintFixed(p)

        if self.floating is not None:
            self.paintFloat(p)

    def paintFixed(self, p):

        outer = Qt.white
        inner = Qt.black

        p.setPen(QPen(outer, 2, Qt.SolidLine))
        p.setBrush(QBrush(inner, Qt.SolidPattern))

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y, x] == 0:
                    p.setBrush(QBrush(inner, Qt.SolidPattern))
                else:
                    p.setBrush(QBrush(QColor(self.colour_table[int(self.board[y, x])]), Qt.SolidPattern))
                p.drawRect(self.x_cell_corners[x], self.y_cell_corners[y], 30, 30)

    def paintFloat(self, p):

        outer = Qt.white
        inner = QColor(self.colour_table[self.floating.identity.value])

        p.setPen(QPen(outer, 2, Qt.SolidLine))
        p.setBrush(QBrush(inner, Qt.SolidPattern))

        for positions in self.floating.coordinates:

            if positions[0] > -1 and positions[1] > -1:
                center_x = self.x_cell_corners[positions[0]]
                center_y = self.y_cell_corners[positions[1]]
                p.drawRect(center_x, center_y, 30, 30)

    def start_game(self):
        self.floating = Tetromino(self.start_pos)
        self.game_status = Status.PLAYING
        self.changed_game_status.emit(self.game_status)
        self.frame_timer.start(self.speed, self)

    def resume_game(self):
        self.game_status = Status.PLAYING
        self.changed_game_status.emit(self.game_status)
        self.frame_timer.start(self.speed, self)

    def pause_game(self):
        self.game_status = Status.PAUSED
        self.changed_game_status.emit(self.game_status)
        self.frame_timer.stop()

    def end_game(self):
        self.game_status = Status.GAMEOVER
        self.changed_game_status.emit(self.game_status)
        self.frame_timer.stop()

    def timerEvent(self, event):

        if event.timerId() == self.frame_timer.timerId():

            if not self.soft_drop_timer.isActive():
                self.gravity()

        elif event.timerId() == self.soft_drop_timer.timerId():
            self.drop_floating()
            self.soft_drop_timer.stop()

        elif event.timerId() == self.left_move_arr_timer.timerId():
            self.move_floating_piece(-1, 0)
            self.update()

        elif event.timerId() == self.left_move_das_timer.timerId():
            if self.left_key_enter_das:
                self.move_floating_piece(-1, 0)
                self.update()
                self.left_move_das_timer.stop()
                self.left_key_enter_das = False
                self.left_move_arr_timer.start(self.arr_speed, self)

        elif event.timerId() == self.right_move_arr_timer.timerId():
            self.move_floating_piece(1, 0)
            self.update()

        elif event.timerId() == self.right_move_das_timer.timerId():
            if self.right_key_enter_das:
                self.move_floating_piece(1, 0)
                self.update()
                self.right_move_das_timer.stop()
                self.right_key_enter_das = False
                self.right_move_arr_timer.start(self.arr_speed, self)

        else:
            super(TetrisBoard, self).timerEvent(event)

    def gravity(self):
        if self.move_floating_piece(0, 1):
            self.update()
        else:
            self.fix_floating_piece()
            self.clear_full_rows()
            self.create_new_piece()

    def drop_floating(self):
        while self.move_floating_piece(0, 1):
            self.update()
        self.fix_floating_piece()
        self.clear_full_rows()
        self.update()
        self.create_new_piece()

    def move_floating_piece(self, x, y):

        if self.check_floating_valid(x, y):
            self.floating.move_by(x, y)
            return True
        else:
            return False

    def check_floating_valid(self, x, y):

        for positions in self.floating.coordinates:
            new_x = positions[0] + x
            new_y = positions[1] + y
            if new_x >= self.width or new_x < 0 or new_y >= self.height:
                return False

            if new_y > -1 and self.board[new_y, new_x] != 0:
                return False

        return True

    def fix_floating_piece(self):

        for positions in self.floating.coordinates:
            if 0 <= positions[0] < self.width and 0 <= positions[1] < self.height:
                self.board[positions[1], positions[0]] = self.floating.identity.value

    def create_new_piece(self):
        self.floating.update_center(self.start_pos[0], self.start_pos[1])
        self.floating.random_assign_shape()

        for positions in self.floating.coordinates:
            if positions[0] > -1 and positions[1] > -1:
                if self.board[positions[1], positions[0]] != 0:
                    self.end_game()
                    return

        self.update()

    def rotate_floating_piece(self, direction):
        if direction == Direction.LEFT:
            self.floating.rotate_right()
            is_valid = False
            for positions in self.floating.wall_kick_offset(Direction.LEFT):
                if self.check_floating_valid(positions[0], positions[1]):
                    self.move_floating_piece(positions[0], positions[1])
                    self.update()
                    is_valid = True
                    break
            if not is_valid:
                self.floating.rotate_left()

        elif direction == Direction.RIGHT:
            self.floating.rotate_left()
            if self.check_floating_valid(0, 0):
                self.update()
            else:
                self.floating.rotate_right()

    def keyPressEvent(self, event):

        key = event.key()

        if self.game_status == Status.NOT_BEGUN and key == Qt.Key_Return:
            self.start_game()

        if key == Qt.Key_P:
            if self.game_status == Status.PAUSED:
                self.resume_game()
            elif self.game_status == Status.PLAYING:
                self.pause_game()

        if self.game_status == Status.PAUSED or self.game_status == Status.GAMEOVER or self.game_status == Status.NOT_BEGUN:
            super(TetrisBoard, self).keyPressEvent(event)
            return

        if key == Qt.Key_Left:
            if not event.isAutoRepeat():
                self.move_floating_piece(-1, 0)
                self.left_key_enter_das = True
                self.left_move_das_timer.start(self.das_speed, self)

        elif key == Qt.Key_Right:
            if not event.isAutoRepeat():
                self.move_floating_piece(1, 0)
                self.right_key_enter_das = True
                self.right_move_das_timer.start(self.das_speed, self)

        elif key == Qt.Key_Down:
            if not self.move_floating_piece(0, 1):
                self.soft_drop_timer.start(self.soft_drop_timer_speed, self)
        elif key == Qt.Key_Up:
            print("Up key pressed")
            if time.time() - self.up_key_last_released > 0.025:
                self.rotate_floating_piece(Direction.LEFT)
        elif key == Qt.Key_Space:
            self.drop_floating()

        self.update()

    def keyReleaseEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.up_key_last_released = time.time()
            # print("Up key released")

        elif key == Qt.Key_Left:
            if not event.isAutoRepeat():
                self.left_key_enter_das = False
                self.left_move_arr_timer.stop()
                self.left_move_das_timer.stop()

        elif key == Qt.Key_Right:
            if not event.isAutoRepeat():
                self.right_key_enter_das = False
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
