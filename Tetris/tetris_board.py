# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np


class TetrisBoard(QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.width = 10
        self.height = 20
        self.speed = 300
        self.cell_side_length = 30

        self.x_cell_corners = np.zeros(10)
        for x in range(self.width):
            self.x_cell_corners[x] = x * self.cell_side_length + 5

        self.y_cell_corners = np.zeros(20)
        for y in range(self.height):
            self.y_cell_corners[y] = y * self.cell_side_length + 5

        self.timer = QBasicTimer()
        self.timer.start(self.speed, self)

    def paintEvent(self, event):

        # Creates the painter object and does things to it
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.paintFixed(p)
        self.paintFloat(p)

    def paintFixed(self, p):

        p.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        p.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        for y in range(self.height):
            for x in range(self.width):
                p.drawRect(self.x_cell_corners[x], self.y_cell_corners[y], 30, 30)

    def paintFloat(self, p):
        print("wow")

    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():

            # if self.isWaitingAfterLine:
            #     self.isWaitingAfterLine = False
            #     self.newPiece()
            # else:
            #     self.oneLineDown()
            print("1r")

        else:
            super(TetrisBoard, self).timerEvent(event)
