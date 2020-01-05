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
        self.is_seeded = False
        self.is_valid = True

    def paintEvent(self, event):

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()
        cell_center = int(self.size / 2)

        if self.selected_state == 0:
            outer, inner = Qt.gray, Qt.gray
            p.fillRect(r, QBrush(inner))
            pen = QPen(outer)
            pen.setWidth(1)
            p.setPen(pen)
            p.drawRect(r)

        elif self.selected_state == 1:
            outer, inner = Qt.black, Qt.white
            if not self.is_valid:
                outer = Qt.red
            pen = QPen(outer, 1.5, Qt.SolidLine)
            p.setPen(pen)
            p.setBrush(QBrush(inner, Qt.SolidPattern))
            p.drawEllipse(r)

            if self.is_seeded:
                pen = QPen(Qt.darkGray, 4, Qt.SolidLine)
                p.setPen(pen)
                p.drawPoint(cell_center, cell_center)

        elif self.selected_state == -1:
            outer, inner = Qt.black, Qt.black
            if not self.is_valid:
                outer = Qt.red
            pen = QPen(outer, 1.5, Qt.SolidLine)
            p.setPen(pen)
            p.setBrush(QBrush(inner, Qt.SolidPattern))
            p.drawEllipse(r)

            if self.is_seeded:
                pen = QPen(Qt.lightGray, 4, Qt.SolidLine)
                p.setPen(pen)
                p.drawPoint(cell_center, cell_center)

    def mousePressEvent(self, e):

        if not self.is_seeded:
            if e.button() == Qt.RightButton:
                if self.selected_state == 0:
                    self.selected_state = 1
                elif self.selected_state == 1:
                    self.selected_state = -1
                elif self.selected_state == -1:
                    self.selected_state = 0

            elif e.button() == Qt.LeftButton:
                if self.selected_state == 0:
                    self.selected_state = -1
                elif self.selected_state == 1:
                    self.selected_state = 0
                elif self.selected_state == -1:
                    self.selected_state = 1

            self.clicked.emit(self.x, self.y, self.selected_state)
            self.update()

    def reset_cell(self):
        self.selected_state = 0
        self.is_seeded = False
        self.is_valid = True
        self.update()
