# Takuzu made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

# Necessary imports
import sys
from takuzu_controller import Controller
from PyQt5.QtWidgets import *


if __name__ == '__main__':
    app = QApplication([])
    controller = Controller()
    controller.begin()
    sys.exit(app.exec_())
