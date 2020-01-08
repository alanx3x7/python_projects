# Binairo controller class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

# Import the individual windows
from binairo_edit_window import EditWindow
from binairo_main_window import MainWindow


class Controller:
    """ Main controller class to control interaction between the two PyQt windows
    """

    def __init__(self):

        # Sets up the default board parameters
        default_x = 10
        default_y = 10
        default_starting = int(default_x * default_y * 0.38)
        default_hint = 3

        # Creates the edit window and links the signal to show_main_window
        self.edit_window = EditWindow()
        self.edit_window.switch_window.connect(self.show_main_window)

        # Creates the main window and links the signal to show_edit_window
        self.main_window = MainWindow(default_x, default_y, default_starting, default_hint)
        self.main_window.switch_window.connect(self.show_edit_window)

    def begin(self):
        """ Called to start the program. Shows the main window and hides the edit window
        """

        self.main_window.show()
        self.edit_window.hide()

    def show_edit_window(self):
        """ Called when signal sent from main window. Shows the edit window and hides main window.
        """

        self.edit_window.show()
        self.main_window.hide()

    def show_main_window(self, x, y, seed, hint):
        """ Called when signal sent from edit window. Shows the main window and possibly modifies it
        :param x: The x dimension of the main window board
        :param y: The y dimension of the main window board
        :param seed: The number of starting cells of the main window board
        :param hint: The number of cells added per hint in the main window board
        """

        self.edit_window.hide()

        # If the x dimension is not zero, then we know that the dimensions or difficulty of board must be changed
        if x != 0:
            self.main_window.destroy()                                      # We destroy the previous main window
            self.main_window = MainWindow(x, y, seed, hint)                 # Create a new main window with parameters
            self.main_window.switch_window.connect(self.show_edit_window)   # Connect the signal to the correct function

        # Otherwise no changes are needed, so we simply show the main window
        else:
            self.main_window.show()
