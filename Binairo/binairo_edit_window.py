
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EditWindow(QMainWindow):

    switch_window = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = 'Alan\'s Binairo'          # Name of the window to be opened
        self.setWindowTitle(self.title)         # Sets the name of the window to be the title

        # Creates a widget object, a vertical box object, and a horizontal box object
        self.first_window = QWidget()
        vb = QVBoxLayout()
        hb_top = QHBoxLayout()
        hb_bottom = QHBoxLayout()

        # Create a button to reset the board
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(QSize(64, 32))
        self.reset_button.pressed.connect(self.reset_button_click)
        hb_top.addWidget(self.reset_button, 0, Qt.Alignment())

        # Create a status label
        self.game_state_label = QLabel()
        self.game_state_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        f = self.game_state_label.font()  # Sets the font
        f.setPointSize(10)
        f.setWeight(75)
        self.game_state_label.setFont(f)
        self.game_state_label.setText("Generating puzzle")
        hb_top.addWidget(self.game_state_label, 0, Qt.Alignment())  # Adds the status label to the horizontal box

        # Create a button to solve the board
        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setFixedSize(QSize(64, 32))
        hb_top.addWidget(self.solve_button, 0, Qt.Alignment())  # Adds the button to the horizontal box

        # Add the horizontal box to the vertical box
        vb.addLayout(hb_top)

        self.first_window.setLayout(vb)
        self.setCentralWidget(self.first_window)

    def reset_button_click(self):
        self.switch_window.emit()
