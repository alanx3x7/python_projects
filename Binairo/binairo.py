import sys
from binairo_main_window import MainWindow
from binairo_controller import Controller
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication([])
    controller = Controller()
    controller.show_main_window()
    sys.exit(app.exec_())