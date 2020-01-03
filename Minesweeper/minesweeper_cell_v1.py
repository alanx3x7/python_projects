# Minesweeper cell class file made from PyQt5
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
    """ Cell object that represents each space in the minefield
    """

    # The signals that are to be sent depending on the actions taken
    oh_no = pyqtSignal()                    # Emitted when the cell is clicked and a mine
    flagged = pyqtSignal(int)               # Emitted when the cell is flagged or unflagged
    clicked = pyqtSignal(int, int)          # Emitted when the cell is clicked
    expandable = pyqtSignal(int, int)       # Emitted when the cell is clicked and has no adjacent mines
    double_clicked = pyqtSignal(int, int)   # Emitted when the cell is double clicked

    def __init__(self, x, y, *args, **kwargs):
        """ Initializes the cell object
        :param x: The x coordinate of the cell
        :param y: The y coordinate of the cell
        """
        super(Cell, self).__init__(*args, **kwargs)

        # Sets the size and the position of the cell
        self.button_size = 40
        self.setFixedSize(QSize(self.button_size, self.button_size))
        self.x = x
        self.y = y

        # Set up the parameters
        self.is_revealed = False            # Tracks whether cell is revealed or not
        self.is_flagged = False             # Tracks whether cell is flagged or not
        self.is_mine = False                # Tracks whether the cell is a mine
        self.num_adjacent = 0               # Tracks number of adjacent mines
        self.mouse_clicks = 0               # Counter for whether double click is occurring
        self.is_double_click = False        # Tracks whether the cell has been doubled clicked or not

    def reset_cell(self):
        """ Re-initializes certain parameters of the cell when game is started anew
        """

        self.is_revealed = False            # Updates so that the cell is not revealed
        self.is_flagged = False             # Updates so that the cell is not flagged
        self.is_mine = False                # Updates so that the cell is not a mine
        self.num_adjacent = 0               # Resets counter for number of adjacent mines
        self.update()                       # Updates the appearance of the cell

    def paintEvent(self, event):
        """ Draws the object
        :param event: The event that triggers this
        """
        p = QPainter(self)                      # Creates the painter for this cell object
        p.setRenderHint(QPainter.Antialiasing)  # I'm not sure what this is
        r = event.rect()                        # I'm not sure what this is either

        # If the cell is supposed to be revealed
        if self.is_revealed:
            if self.is_mine:                    # If it is a mine, insert a picture of a mine
                p.drawPixmap(r, QPixmap(IMAGE_MINE))
            elif self.num_adjacent == 0:        # If it has no adjacent mines, insert picture of background grey
                p.drawPixmap(r, QPixmap(IMAGE_GRAY))
            else:                               # Else it should display the number of adjacent mines
                pen = QPen(Qt.black)
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.num_adjacent))
                p.fillRect(r, QBrush(QColor(128, 128, 255, 128)))

        # If the cells is supposed to be flagged, insert picture of a flag
        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMAGE_FLAG))

        # If the cell is not supposed to be revealed nor is it flagged, have to draw a cyan box
        else:
            outer, inner = Qt.darkBlue, Qt.cyan
            p.fillRect(r, QBrush(inner))
            pen = QPen(outer)
            pen.setWidth(1)
            p.setPen(pen)
            p.drawRect(r)

    def reveal(self):
        """ Reveals the cell
        """

        # Updates the status and appearance of the cell
        self.is_revealed = True
        self.update()

        # Send a clicked signal
        self.clicked.emit(self.x, self.y)

        # If there are no adjacent bombs, send an expandable signal
        if self.num_adjacent == 0:
            self.expandable.emit(self.x, self.y)

    def click(self):
        """ Called when the cell is clicked
        """

        if not self.is_revealed:
            self.reveal()               # Reveals the cell if it is not already revealed

    def flag(self):
        """ Called when the cell is right-clicked
        """

        # If the cell is not revealed or flagged, we flag it and send a flagged signal
        if not self.is_flagged and not self.is_revealed:
            self.is_flagged = True
            self.update()
            self.flagged.emit(1)

        # If the cell is not revealed and is flagged, we unflag it and send a flagged signal (signifying unflagged)
        elif self.is_flagged and not self.is_revealed:
            self.is_flagged = False
            self.update()
            self.flagged.emit(-1)

    def mousePressEvent(self, e):
        """ Called when the cell is clicked on by a mouse button. Updates the number of clicks currently on the cell
        :param e: The mouse button click event
        """
        self.mouse_clicks = self.mouse_clicks + 1

    def mouseReleaseEvent(self, e):
        """ Called when the mouse click on the cell is released.
        :param e: The mouse button release event
        """

        # Checks that the mouse is released over the same cell it was pressed on
        # Note (0, 0) is the top left corner of the cell, so only needs to be within button size of origin
        if -5 <= e.x() <= self.button_size + 5:
            if -5 <= e.y() <= self.button_size + 5:

                # If the number of clicks was 2, we know this is a double click, so we set that to true
                if self.mouse_clicks == 2:
                    self.is_double_click = True

                    # If the cell is already revealed, then we emit the double click signal for non-flag reveal
                    if self.is_revealed:
                        self.double_clicked.emit(self.x, self.y)

                # If the cell was double clicked, we do nothing when the second click is released
                elif self.is_double_click:
                    self.is_double_click = False

                # If the single click was the right click and not revealed, set the flag
                elif e.button() == Qt.RightButton and not self.is_revealed:
                    self.flag()

                # If it was the left click, reveal it
                elif e.button() == Qt.LeftButton:
                    self.click()

                    # If a mine is revealed, we emit a game over signal
                    if self.is_mine:
                        self.oh_no.emit()

        # We update the number of clicks on the current cell
        self.mouse_clicks = self.mouse_clicks - 1
