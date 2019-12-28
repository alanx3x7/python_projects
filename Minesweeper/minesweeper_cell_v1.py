
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


IMAGE_MINE = QImage("./images/mine.jpg")
IMAGE_FLAG = QImage("./images/flag.jpg")


class Cell(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    oh_no = pyqtSignal()

    def __init__(self, x, y, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)

        # Sets the size and the position of the cell
        self.button_size = 20
        self.setFixedSize(QSize(self.button_size, self.button_size))
        self.x = x
        self.y = y

        # Set up the parameters
        self.is_revealed = False
        self.is_flagged = False
        self.is_bomb = False
        self.initially_clicked = False

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()
        outer, inner = Qt.gray, Qt.lightGray
        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            outer, inner = Qt.blue, Qt.blue
            p.fillRect(r, QBrush(inner))
            pen = QPen(outer)
            pen.setWidth(1)
            p.setPen(pen)
            p.drawRect(r)

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMAGE_FLAG))

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            # if self.adjacent_n == 0:
            #     self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def flag(self):
        if not self.is_flagged or not self.is_revealed:
            self.is_flagged = True
            self.update()

    def mouseReleaseEvent(self, e):

        # Checks that the mouse is released over the same cell it was pressed on
        # Note (0, 0) is the top left corner of the cell, so only needs to be within button size of origin
        if 0 <= e.x() <= self.button_size:
            if 0 <= e.y() <= self.button_size:

                # If it was the right click and not revealed, set the flag
                if e.button() == Qt.RightButton and not self.is_revealed:
                    self.flag()

                # If it was the left click, reveal it
                elif e.button() == Qt.LeftButton:
                    self.click()
                    # if self.is_mine:
                    #     self.oh_no.emit()
