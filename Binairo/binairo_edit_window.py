
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EditWindow(QMainWindow):

    switch_window = pyqtSignal(int, int, int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Binairo'          # Name of the window to be opened
        self.setWindowTitle(self.title)         # Sets the name of the window to be the title

        self.board_x_size = 12
        self.board_y_size = 12
        self.num_initial_seed = int(self.board_x_size * self.board_y_size * 0.23)
        self.num_added_hint = 3

        # Creates a widget object, a vertical box object, and a horizontal box object
        self.first_window = QWidget()
        vb_radio = QVBoxLayout()
        vb_main = QVBoxLayout()
        hb_top = QHBoxLayout()
        hb_bottom = QHBoxLayout()

        # Create radio buttons
        for i in range(8):
            radio_button = QRadioButton("%d x %d" % (i * 2 + 4, i * 2 + 4))
            if i == 0: radio_button.setChecked(True)
            radio_button.size = i * 2 + 4
            radio_button.toggled.connect(self.radio_selected)
            vb_radio.addWidget(radio_button)

        # Create a button to reset the board
        self.reset_button = QPushButton("Back", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.pressed.connect(self.reset_button_click)
        hb_bottom.addWidget(self.reset_button, 0, Qt.Alignment())

        # Create a status label
        self.game_state_label = QLabel()
        self.game_state_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.game_state_label.font()  # Sets the font
        f.setPointSize(10)
        f.setWeight(75)
        self.game_state_label.setFont(f)
        self.game_state_label.setText("Generating puzzle")
        hb_bottom.addWidget(self.game_state_label, 0, Qt.Alignment())  # Adds the status label to the horizontal box

        # Create a button to solve the board
        self.save_button = QPushButton("Save", self)
        self.save_button.setFixedSize(QSize(64, 32))
        self.save_button.pressed.connect(self.save_button_click)
        hb_bottom.addWidget(self.save_button, 0, Qt.Alignment())  # Adds the button to the horizontal box

        # Add the horizontal box to the vertical box
        vb_main.addLayout(vb_radio)
        vb_main.addLayout(hb_top)
        vb_main.addLayout(hb_bottom)

        self.first_window.setLayout(vb_main)
        self.setCentralWidget(self.first_window)

    def reset_button_click(self):
        self.switch_window.emit(0, 0, 0, 0)

    def save_button_click(self):
        self.switch_window.emit(self.board_x_size, self.board_y_size, self.num_initial_seed, self.num_added_hint)

    def radio_selected(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.board_x_size = radio_button.size
            self.board_y_size = radio_button.size
            self.num_initial_seed = int(self.board_x_size * self.board_y_size * 0.23)
