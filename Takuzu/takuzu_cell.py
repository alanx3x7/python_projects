# Takuzu cell class file made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

# PyQt5 imports
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Images for the cells to display depending on status
IMAGE_MINE = QImage("./images/mine.jpg")
IMAGE_FLAG = QImage("./images/flag.jpg")
IMAGE_GRAY = QImage("./images/gray.png")


class Cell(QWidget):
    """ Main class file for the binairo cells
    """

    # Signal to be sent to main window when the cell is clicked
    clicked = pyqtSignal(int, int, int)

    def __init__(self, x, y, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)

        # Sets the default size of the cell
        self.size = 40
        self.setFixedSize(QSize(self.size, self.size))

        # Parameters to hold the characteristics of the cell itself
        self.x = x                          # x coordinate of the cell in the board
        self.y = y                          # y coordinate of the cell in the board
        self.selected_state = 0             # The current state of the cell (0 if blank, 1 if white, -1 if black)
        self.is_seeded = False              # Whether the cell is seeded (cannot be changed by user)
        self.is_valid = True                # Whether the cell is valid (False the cell violates a rule)

    def paintEvent(self, event):
        """ Called to draw the cell on the board.
        :param event: Something that triggers the calling of this function
        """

        # Creates the painter object and does things to it
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()

        # Finds the center of the cell in cell coordinates to draw shapes correctly
        cell_center = int(self.size / 2)

        # If the cell is supposed to be blank, we draw a gray rectangle background
        if self.selected_state == 0:
            outer, inner = Qt.gray, Qt.gray                 # We set it to have gray center and border
            p.fillRect(r, QBrush(inner))                    # We draw a rectangle
            pen = QPen(outer)
            pen.setWidth(1)
            p.setPen(pen)
            p.drawRect(r)

        # If the cell is supposed to be white
        elif self.selected_state == 1:
            outer, inner = Qt.black, Qt.white               # We set it to be a white circle with black border
            if not self.is_valid:                           # If the cell is invalid, we set a red border instead
                outer = Qt.red
            pen = QPen(outer, 1.5, Qt.SolidLine)            # We set border to be a solid line of thickness 1.5
            p.setPen(pen)
            p.setBrush(QBrush(inner, Qt.SolidPattern))
            p.drawEllipse(r)                                # We draw a circle

            if self.is_seeded:                              # If the cell is seeded
                pen = QPen(Qt.darkGray, 4, Qt.SolidLine)    # We draw a dark grey point in the center of the circle
                p.setPen(pen)
                p.drawPoint(cell_center, cell_center)

        # If the cell is supposed to be black
        elif self.selected_state == -1:
            outer, inner = Qt.black, Qt.black               # We set it to be a black circle with black border
            if not self.is_valid:                           # If the cell is invalid, we set a red border instead
                outer = Qt.red
            pen = QPen(outer, 1.5, Qt.SolidLine)            # We set border to be a solid line of thickness 1.5
            p.setPen(pen)
            p.setBrush(QBrush(inner, Qt.SolidPattern))
            p.drawEllipse(r)                                # We draw a circle

            if self.is_seeded:                              # If the cell is seeded
                pen = QPen(Qt.lightGray, 4, Qt.SolidLine)   # We draw a light grey point in the center of the circle
                p.setPen(pen)
                p.drawPoint(cell_center, cell_center)

    def mousePressEvent(self, e):
        """ Called when the mouse presses on the cell.
        :param e: The event that triggers the function
        """

        # Only do something when the cell is not seeded and allowed to be changed by the user
        if not self.is_seeded:

            # If the button is a right click
            if e.button() == Qt.RightButton:
                if self.selected_state == 0:            # If it is blank, it should now be white
                    self.selected_state = 1
                elif self.selected_state == 1:          # If it is white, it should now be black
                    self.selected_state = -1
                elif self.selected_state == -1:         # If it is black, it should now be blank
                    self.selected_state = 0

            # If the button is a left click
            elif e.button() == Qt.LeftButton:
                if self.selected_state == 0:            # If it is blank, it should now be black
                    self.selected_state = -1
                elif self.selected_state == 1:          # If it is white, it should now be blank
                    self.selected_state = 0
                elif self.selected_state == -1:         # If it is black, it should now be white
                    self.selected_state = 1

            # Emits signal to main window to let it know it has been clicked
            self.clicked.emit(self.x, self.y, self.selected_state)

            # Updates the appearance of the cell
            self.update()

    def reset_cell(self):
        """ Called when the cell needs to be reset to default parameters
        """

        self.selected_state = 0                         # Cell should be blank
        self.is_seeded = False                          # Cell should not be seeded
        self.is_valid = True                            # Cell should be valid
        self.update()                                   # Update appearance of the cell
