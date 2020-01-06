
from binairo_edit_window import EditWindow
from binairo_main_window import MainWindow


class Controller:

    def __init__(self):
        default_x = 12
        default_y = 12
        default_starting = int(default_x * default_y * 0.23)
        default_hint = 3
        self.edit_window = EditWindow()
        self.main_window = MainWindow(default_x, default_y, default_starting, default_hint)
        self.edit_window.switch_window.connect(self.show_main_window)
        self.main_window.switch_window.connect(self.show_edit_window)

    def begin(self):
        self.main_window.show()
        self.edit_window.hide()

    def show_edit_window(self):
        self.edit_window.show()
        self.main_window.hide()

    def show_main_window(self, x, y, seed, hint):
        self.edit_window.hide()
        if x != 0:
            self.main_window.destroy()
            self.main_window = MainWindow(x, y, seed, hint)
            self.main_window.switch_window.connect(self.show_edit_window)
        else:
            self.main_window.show()
