# Binairo cell class file made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/03

# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Images for the cells to display depending on status
IMAGE_MINE = QImage("./images/mine.jpg")
IMAGE_FLAG = QImage("./images/flag.jpg")
IMAGE_GRAY = QImage("./images/gray.png")


class Cell(QWidget):

    clicked = pyqtSignal(int, int, int)

    def __init__(self, x, y, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)

        self.size = 40
        self.setFixedSize(QSize(self.size, self.size))

        self.x = x
        self.y = y
        self.selected_state = 0
        self.real_state = 0

    def paintEvent(self, event):

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()

        if self.selected_state == 0:
            outer, inner = Qt.gray, Qt.gray
            p.fillRect(r, QBrush(inner))
            pen = QPen(outer)
            pen.setWidth(1)
            p.setPen(pen)
            p.drawRect(r)

        elif self.selected_state == 1:
            outer, inner = Qt.black, Qt.white
            pen = QPen(outer, 1, Qt.SolidLine)
            p.setPen(pen)
            p.setBrush(QBrush(inner, Qt.SolidPattern))
            p.drawEllipse(r)

        elif self.selected_state == 2:
            outer, inner = Qt.black, Qt.black
            pen = QPen(outer, 1, Qt.SolidLine)
            p.setPen(pen)
            p.setBrush(QBrush(inner, Qt.SolidPattern))
            p.drawEllipse(r)

    def mousePressEvent(self, e):

        if e.button() == Qt.RightButton:
            if self.selected_state == 0:
                self.selected_state = 1
            elif self.selected_state == 1:
                self.selected_state = 2
            elif self.selected_state == 2:
                self.selected_state = 0

        elif e.button() == Qt.LeftButton:
            if self.selected_state == 0:
                self.selected_state = 2
            elif self.selected_state == 1:
                self.selected_state = 0
            elif self.selected_state == 2:
                self.selected_state = 1

        self.clicked.emit(self.x, self.y, self.selected_state)
        self.update()
