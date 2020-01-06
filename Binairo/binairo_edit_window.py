
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

DIFFICULTIES = {
    0: "Beginner",
    1: "Easy",
    2: "Medium",
    3: "Hard",
    4: "Expert"
}


class EditWindow(QMainWindow):

    switch_window = pyqtSignal(int, int, int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Binairo'          # Name of the window to be opened
        self.setWindowTitle(self.title)         # Sets the name of the window to be the title

        self.board_x_size = 10
        self.board_y_size = 10
        self.num_cells_start = int(self.board_x_size * self.board_y_size * 0.38)
        self.num_added_hint = 3

        # Creates a widget object, a vertical box object, and a horizontal box object
        self.first_window = QWidget()
        vb_size_radio = QVBoxLayout()
        vb_diff_radio = QVBoxLayout()
        vb_main = QVBoxLayout()
        hb_top = QHBoxLayout()
        hb_bottom = QHBoxLayout()

        # Create radio buttons to change board size
        size_group_box = QGroupBox("Change Board Size")
        for i in range(8):
            radio_button = QRadioButton("%d x %d" % (i * 2 + 4, i * 2 + 4))
            if i == 3:
                radio_button.setChecked(True)
            radio_button.size = i * 2 + 4
            radio_button.toggled.connect(self.radio_selected)
            vb_size_radio.addWidget(radio_button, 0, Qt.Alignment())
        size_group_box.setLayout(vb_size_radio)
        hb_top.addWidget(size_group_box, 0, Qt.Alignment())

        # Create radio buttons to change difficulty
        diff_group_box = QGroupBox("Change Difficulty")
        for i in range(5):
            radio_button2 = QRadioButton(DIFFICULTIES[i])
            if i == 2:
                radio_button2.setChecked(True)
            radio_button2.seed = 0.5 - 0.06 * i
            radio_button2.toggled.connect(self.difficulty_selected)
            vb_diff_radio.addWidget(radio_button2, 0, Qt.Alignment())
        diff_group_box.setLayout(vb_diff_radio)
        hb_top.addWidget(diff_group_box, 0, Qt.Alignment())

        # Create a button to reset the board
        self.reset_button = QPushButton("Back", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.clicked.connect(self.reset_button_click)
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
        self.save_button.clicked.connect(self.save_button_click)
        hb_bottom.addWidget(self.save_button, 0, Qt.Alignment())  # Adds the button to the horizontal box

        # Add the horizontal box to the vertical box
        vb_main.addLayout(hb_top)
        vb_main.addLayout(hb_bottom)

        self.first_window.setLayout(vb_main)
        self.setCentralWidget(self.first_window)

    def reset_button_click(self):
        self.switch_window.emit(0, 0, 0, 0)

    def save_button_click(self):
        self.switch_window.emit(self.board_x_size, self.board_y_size, self.num_cells_start, self.num_added_hint)

    def radio_selected(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.board_x_size = radio_button.size
            self.board_y_size = radio_button.size
            self.num_cells_start = int(self.board_x_size * self.board_y_size * 0.23)

    def difficulty_selected(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.num_cells_start = int(self.board_x_size * self.board_y_size * radio_button.seed)