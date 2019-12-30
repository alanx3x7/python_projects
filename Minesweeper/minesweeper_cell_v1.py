
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


IMAGE_MINE = QImage("./images/mine.jpg")
IMAGE_FLAG = QImage("./images/flag.jpg")
IMAGE_GRAY = QImage("./images/gray.png")


class Cell(QWidget):

    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal(int, int)
    double_clicked = pyqtSignal(int, int)
    oh_no = pyqtSignal()

    def __init__(self, x, y, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)

        # Sets the size and the position of the cell
        self.button_size = 40
        self.setFixedSize(QSize(self.button_size, self.button_size))
        self.x = x
        self.y = y

        # Set up the parameters
        self.is_revealed = False
        self.is_flagged = False
        self.is_mine = False
        self.initially_clicked = False
        self.num_adjacent = 0
        self.mouse_clicks = 0
        self.is_double_click = False

    def reset_cell(self):
        self.is_revealed = False
        self.is_flagged = False
        self.is_mine = False
        self.initially_clicked = False
        self.num_adjacent = 0
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            if self.is_mine:
                p.drawPixmap(r, QPixmap(IMAGE_MINE))
            elif self.num_adjacent == 0:
                p.drawPixmap(r, QPixmap(IMAGE_GRAY))
            else:
                pen = QPen(Qt.black)
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.num_adjacent))
                p.fillRect(r, QBrush(QColor(128, 128, 255, 128)))

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMAGE_FLAG))

        else:
            outer, inner = Qt.darkBlue, Qt.cyan
            p.fillRect(r, QBrush(inner))
            pen = QPen(outer)
            pen.setWidth(1)
            p.setPen(pen)
            p.drawRect(r)

    def reveal(self):
        self.is_revealed = True
        self.update()

        # Send a clicked signal
        self.clicked.emit(self.x, self.y)

        # If there are no adjacent bombs, send an expandable signal
        if self.num_adjacent == 0:
            self.expandable.emit(self.x, self.y)

    def click(self):

        # Reveals if not revealed
        if not self.is_revealed:
            self.reveal()

    def flag(self):
        if not self.is_flagged or not self.is_revealed:
            self.is_flagged = True
            self.update()

    def mousePressEvent(self, e):
        self.mouse_clicks = self.mouse_clicks + 1

    def mouseReleaseEvent(self, e):

        # Checks that the mouse is released over the same cell it was pressed on
        # Note (0, 0) is the top left corner of the cell, so only needs to be within button size of origin
        if -5 <= e.x() <= self.button_size + 5:
            if -5 <= e.y() <= self.button_size + 5:

                if self.mouse_clicks == 2:
                    self.is_double_click = True
                    if self.is_revealed:
                        self.double_clicked.emit(self.x, self.y)

                elif self.is_double_click:
                    self.is_double_click = False

                # If it was the right click and not revealed, set the flag
                elif e.button() == Qt.RightButton and not self.is_revealed:
                    self.flag()

                # If it was the left click, reveal it
                elif e.button() == Qt.LeftButton:
                    self.click()
                    if self.is_mine:
                        self.oh_no.emit()

        self.mouse_clicks = self.mouse_clicks - 1
