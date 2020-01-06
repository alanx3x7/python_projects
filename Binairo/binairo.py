import sys
from binairo_main_window import MainWindow
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())