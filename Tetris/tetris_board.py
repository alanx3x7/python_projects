# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

from tetris_tetromino import Tetromino


class TetrisBoard(QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.width = 10
        self.height = 20
        self.speed = 300
        self.cell_side_length = 30
        self.start_pos = (4, 0)

        self.x_cell_corners = np.zeros(10)
        for x in range(self.width):
            self.x_cell_corners[x] = x * self.cell_side_length + 5

        self.y_cell_corners = np.zeros(20)
        for y in range(self.height):
            self.y_cell_corners[y] = y * self.cell_side_length + 5

        self.board = np.zeros((self.height, self.width))

        self.timer = QBasicTimer()

        self.floating = Tetromino(self.start_pos)

        QApplication.processEvents()

        self.timer.start(self.speed, self)

    def paintEvent(self, event):

        # Creates the painter object and does things to it
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.paintFixed(p)
        self.paintFloat(p)

    def paintFixed(self, p):

        outer = Qt.white
        inner = Qt.black

        p.setPen(QPen(outer, 2, Qt.SolidLine))
        p.setBrush(QBrush(inner, Qt.SolidPattern))

        for y in range(self.height):
            for x in range(self.width):
                p.drawRect(self.x_cell_corners[x], self.y_cell_corners[y], 30, 30)

    def paintFloat(self, p):

        outer = Qt.white
        inner = Qt.green

        p.setPen(QPen(outer, 2, Qt.SolidLine))
        p.setBrush(QBrush(inner, Qt.SolidPattern))

        for positions in self.floating.coordinates:

            if positions[0] > -1 and positions[1] > -1:
                center_x = self.x_cell_corners[positions[0]]
                center_y = self.y_cell_corners[positions[1]]
                p.drawRect(center_x, center_y, 30, 30)

    def timerEvent(self, event):

        # self.floating.random_assign_shape()

        if event.timerId() == self.timer.timerId():

            # if self.isWaitingAfterLine:
            #     self.isWaitingAfterLine = False
            #     self.newPiece()
            # else:
            #     self.oneLineDown()
            self.gravity()
            print(self.floating.identity)

        else:
            super(TetrisBoard, self).timerEvent(event)

    def gravity(self):
        if self.move_floating_piece(0, 1):
            self.update()
        else:
            self.fix_floating_piece()
            self.floating.update_center(self.start_pos[0], self.start_pos[1])
            self.floating.random_assign_shape()
            self.update()

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

        return True

    def fix_floating_piece(self):

        for positions in self.floating.coordinates:
            self.board[positions[1], positions[0]] = self.floating.identity.value
