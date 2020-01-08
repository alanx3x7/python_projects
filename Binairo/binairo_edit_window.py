# Binairo edit class made from PyQt5
# Author: Alan Lai
# Email: alan_lai@jhu.edu
# Version: 1.0
# Last Updated: 2020/01/08

# PyQt5 imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# List of difficulties
DIFFICULTIES = {
    0: "Beginner",
    1: "Easy",
    2: "Medium",
    3: "Hard",
    4: "Expert"
}


class EditWindow(QMainWindow):
    """ Class file for the edit window for changing board size and difficulty
    """

    # Signal sent to the controller when the board size is modified
    switch_window = pyqtSignal(int, int, int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Binairo'          # Name of the window to be opened
        self.setWindowTitle(self.title)         # Sets the name of the window to be the title

        self.board_x_size = 10                  # x dimension of the board
        self.board_y_size = 10                  # y dimension of the board
        self.default_diff = 0.38                # Default difficulty is medium (starts with 38% cells filled)
        self.num_cells_start = int(self.board_x_size * self.board_y_size * self.default_diff)
        self.num_added_hint = 3                 # Number of cells added per hint

        # Creates the objects needed
        self.first_window = QWidget(*args, **kwargs)    # Main widget to hold the boxes
        vb_size_radio = QVBoxLayout()           # Vertical box to hold the size radio buttons
        vb_diff_radio = QVBoxLayout()           # Vertical box to hold the difficulty radio buttons
        vb_main = QVBoxLayout()                 # Main vertical box to hold the horizontal boxes
        hb_top = QHBoxLayout()                  # Horizontal box on top to hold the radio boxes
        hb_bottom = QHBoxLayout()               # Horizontal box on the bottom to hold the buttons

        # Create 8 radio buttons to change board size
        size_group_box = QGroupBox("Change Board Size")                 # Place in group box for organization
        for i in range(8):
            radio_button = QRadioButton("%d x %d" % (i * 2 + 4, i * 2 + 4))
            if i == 3:                                                  # Default is 8 x 8 size
                radio_button.setChecked(True)                           # Set default to checked for now
            radio_button.size = i * 2 + 4
            radio_button.toggled.connect(self.radio_selected)           # Connect to radio_selected
            vb_size_radio.addWidget(radio_button, 0, Qt.Alignment())    # Add to the vertical box
        size_group_box.setLayout(vb_size_radio)                         # Add the box to the group box
        hb_top.addWidget(size_group_box, 0, Qt.Alignment())             # Add the group box to the top horizontal box

        # Create radio buttons to change difficulty
        diff_group_box = QGroupBox("Change Difficulty")                 # Place in group box for organization
        for i in range(5):
            radio_button2 = QRadioButton(DIFFICULTIES[i])
            if i == 2:                                                  # Default is medium difficulty
                radio_button2.setChecked(True)                          # Set default to checked for now
            radio_button2.seed = 0.5 - 0.06 * i
            radio_button2.toggled.connect(self.difficulty_selected)     # Connect to difficulty_selected
            vb_diff_radio.addWidget(radio_button2, 0, Qt.Alignment())   # Add to the vertical box
        diff_group_box.setLayout(vb_diff_radio)                         # Add the box to the group box
        hb_top.addWidget(diff_group_box, 0, Qt.Alignment())             # Add the group box to the to horizontal box

        # Create a button to go back to board without changing settings
        self.back_button = QPushButton("Back", self)
        self.back_button.setFixedSize(QSize(64, 32))
        self.back_button.clicked.connect(self.back_button_click)        # Connect to back_button_click
        hb_bottom.addWidget(self.back_button, 0, Qt.Alignment())        # Add to the bottom horizontal box

        # Create a button to solve the board
        self.save_button = QPushButton("Save", self)
        self.save_button.setFixedSize(QSize(64, 32))
        self.save_button.clicked.connect(self.save_button_click)        # Connect to save_button_click
        hb_bottom.addWidget(self.save_button, 0, Qt.Alignment())        # Add to the bottom horizontal box

        # Create a status label
        self.window_label = QLabel()
        self.window_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.window_label.font()  # Sets the font
        f.setPointSize(10)
        f.setWeight(75)
        self.window_label.setFont(f)
        self.window_label.setText("Edit Settings")
        vb_main.addWidget(self.window_label, 0, Qt.Alignment())         # Adds the label to the horizontal box

        # Add the horizontal boxes to the vertical box
        vb_main.addLayout(hb_top)
        vb_main.addLayout(hb_bottom)

        # Set the window appearance to the main vertical box
        self.first_window.setLayout(vb_main)
        self.setCentralWidget(self.first_window)

    def back_button_click(self):
        """ Called when the back button is clicked - returns to main board without changing settings
        """

        self.switch_window.emit(0, 0, 0, 0)

    def save_button_click(self):
        """ Called when the save button is clicked - changes main board according to selected settings
        """

        self.switch_window.emit(self.board_x_size, self.board_y_size, self.num_cells_start, self.num_added_hint)

    def radio_selected(self):
        """ Called when the size radio buttons are selected. Updates the properties to keep track of selection
        """
        radio_button = self.sender()

        # Only update parameters if the radio button is selected (and nothing when it is unselected)
        if radio_button.isChecked():

            # Updates board size parameters and number of starting cells in accordance to difficulty
            self.board_x_size = radio_button.size
            self.board_y_size = radio_button.size
            self.num_cells_start = int(self.board_x_size * self.board_y_size * self.default_diff)

    def difficulty_selected(self):
        """ Called when the difficulty radio buttons are selected. Updates the properties to keep track of selection
        """

        radio_button = self.sender()

        # Only updates parameters if the radio button is selected (and nothing when it is unselected)
        if radio_button.isChecked():

            # Updates the difficulty parameter and the number of starting cells
            self.default_diff = radio_button.seed
            self.num_cells_start = int(self.board_x_size * self.board_y_size * self.default_diff)
