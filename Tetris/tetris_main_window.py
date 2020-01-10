# Tetris main class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

# Typical imports
import random
import time
import numpy as np

# PyQt5 specific imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Importing the class file for the individual cells
from takuzu_cell import Cell


class MainWindow(QMainWindow):
    """ Main class window for the binairo game
    """

    # Signal when the button to edit board size and difficulty is pressed
    switch_window = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Takuzu'  # Name of the window to be opened
        self.setWindowTitle(self.title)  # Sets the name of the window to be the title

        self.width = 10
        self.height = 20

        self.window = QWidget(*args, **kwargs)
        vb = QVBoxLayout()


