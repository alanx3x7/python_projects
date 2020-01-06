
from binairo_edit_window import EditWindow
from binairo_main_window import MainWindow


class Controller:

    def __init__(self):
        self.edit_window = EditWindow()
        self.main_window = MainWindow()

    def show_edit_window(self):
        self.edit_window.switch_window.connect(self.show_main_window)
        self.edit_window.show()
        self.main_window.hide()

    def show_main_window(self):
        self.main_window.switch_window.connect(self.show_edit_window)
        self.main_window.show()
        self.edit_window.hide()
