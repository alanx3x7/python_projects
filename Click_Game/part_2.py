# Alan Lai, 2019/11/02
# Neocis Coding Challenge

import math
import sys

import numpy as np
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class Window(QMainWindow):
    """ Main class for the application
    """

    def __init__(self):
        super().__init__()
        self.title = "Part 2"           # Title of the application

        self.top = 150                  # Location of application when it is launched
        self.left = 150                 # Location of application when it is launched
        self.width = 600                # Width of initial window
        self.height = 600               # Height of initial window
        self.num_xpoints = 20           # Number of points in x direction
        self.num_ypoints = 20           # Number of points in y direciton

        self.setMouseTracking(True)     # Makes the application able to track the mouse

        self.center = QPoint()          # Sets the center of the circle to be drawn to 0
        self.edge = QPoint()            # Sets the edge of the circle to be 0

        self.init_window()              # Initializes by going to the initialize function

    def init_window(self):
        """ Initializing the application object
        """
        # Sets the title and the shape of the window
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        # For all points, set default colour to gray, and default location to (0, 0)
        # We have a total of (num_xpoints * num_ypoints) points
        self.colourList = [[Qt.gray] * self.num_xpoints for i in range(self.num_ypoints)]
        self.pointLocation = [[(0, 0)] * self.num_xpoints for i in range(self.num_ypoints)]

        # Creates a button that says generate and has a tool tip
        self.button = QPushButton('Generate', self)
        self.button.setToolTip('Click to generate circle that best fits selected points! Select points by clicking')

        # Centers the button at the bottom of the window
        self.button.move(self.width / 2.0 - 50, self.height - 40)
        self.button.resize(100, 32)
        self.button.clicked.connect(self.on_click)

        # Show the window
        self.show()

    def paintEvent(self, event):
        """ Generates the scene by drawing all the relevant objects
        :param event: The triggering event, could be window resize, or initialization
        """
        # Initializes the Painter object
        qp = QPainter()
        qp.begin(self)

        self.drawSpace(qp)              # Draws the box for the points
        self.drawPoint(qp)              # Draw the points
        self.drawTheCircle(qp)          # Draws the circles if there are any
        qp.end()

    def drawSpace(self, qp):
        """ Draws the white background bounding box for the dots
        :param qp: The painter object
        """
        qp.setPen(QPen(Qt.white, 8, Qt.SolidLine))          # White border
        qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))      # White background fill
        size = self.size()                                  # Gets current size of window

        # Draws it so that it has a margin of 50 from each end of the window
        qp.drawRect(50, 50, size.width() - 100, size.height() - 100)

    def drawPoint(self, qp):
        """ Draws all of the points in the window
        :param qp: The painter object
        """
        size = self.size()

        # Loops through every point in the window
        for i in range(self.num_xpoints):
            for j in range(self.num_ypoints):

                # Evenly distribute the points in both the x and y directions
                x_coord = ((size.width() - 100) / 21.0) * (i + 1) + 50
                y_coord = ((size.height() - 100) / 21.0) * (j + 1) + 50

                # Colours are determined by colourList
                qp.setPen(QPen(self.colourList[i][j], 1, Qt.SolidLine))
                qp.setBrush(QBrush(self.colourList[i][j], Qt.SolidPattern))

                # We draw the points as rectangles, and updates their locations
                qp.drawRect(x_coord, y_coord, 10, 10)
                self.pointLocation[i][j] = (x_coord, y_coord)

    def drawTheCircle(self, qp):
        """ Draws the circle if the user has clicked and dragged.
            If the user has not dragged, then the radius is 0 and no circle is drawn
        :param qp: The painter object
        """
        # The circle should be opaque, hence brush transparency is forced to be 0
        qp.setBrush(QBrush(QColor(100, 10, 10, 0)))

        # Finds the x and y distances, and radius from the center to the edge of the circle
        x_diff = self.edge.x() - self.center.x()
        y_diff = self.edge.y() - self.center.y()
        radius = math.sqrt(x_diff * x_diff + y_diff * y_diff)

        # Draws the blue circle based on the edge location
        qp.setPen(QPen(Qt.blue, 4, Qt.SolidLine))
        qp.drawEllipse(self.center, radius, radius)

    def mousePressEvent(self, event):
        """ Called when the mouse is pressed. Toggle point where clicked happened between gray and blue
        :param event: The event object representing the click of the mouse
        """
        # Loops through all points to find the point where mouse button was clicked
        for i in range(self.num_xpoints):
            for j in range(self.num_ypoints):

                # Works out distance to mouse click
                x_diff = event.x() - self.pointLocation[i][j][0]
                y_diff = event.y() - self.pointLocation[i][j][1]
                distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)

                # Toggles between marked (blue) and unmarked (gray) if that point is clicked
                if distance < 10:
                    if self.colourList[i][j] == Qt.gray:
                        self.colourList[i][j] = Qt.blue
                    else:
                        self.colourList[i][j] = Qt.gray

        # Update to show the change in the screen
        self.update()

    def find_marked_points(self):
        """ Finds the points in the grid that are blue/marked
        :return: x: the x coordinates of those marked points (1d vector)
                 y: the y coordinates of those marked points (1d vector)
        """
        x = np.array([])
        y = np.array([])

        # Loops through all of the points
        for i in range(self.num_xpoints):
            for j in range(self.num_ypoints):
                # Adds those points if they are blue/marked
                if self.colourList[i][j] == Qt.blue:
                    x = np.append(x, self.pointLocation[i][j][0])
                    y = np.append(y, self.pointLocation[i][j][1])

        return x, y

    def solve_least_squares_circle(self, x, y):
        """ Finds the least squares solution for circle best fitting the marked points
        :param x: The x coordinates of the marked points
        :param y: The y coordinates of the marked points
        :return xc: The x coordinate of the center of circle
                yc: The y coordinate of the center of circle
                rad: The radius of the circle
        """
        # First normalizes the coordinates so they center about 0, 0
        u = x - np.mean(x)
        v = y - np.mean(y)

        # Sets up the least squares matrix values
        suv = np.sum(u * v)
        suu = np.sum(u ** 2)
        svv = np.sum(v ** 2)
        suuv = np.sum(u ** 2 * v)
        suvv = np.sum(u * v ** 2)
        suuu = np.sum(u ** 3)
        svvv = np.sum(v ** 3)

        # Forms the least squares matrices and solve for them
        A = np.array([[suu, suv], [suv, svv]])
        B = np.array([suuu + suvv, svvv + suuv]) / 2.0
        uc, vc = np.linalg.solve(A, B)

        # Find the center coordinates by re-adding the mean
        xc = np.mean(x) + uc
        yc = np.mean(y) + vc

        # Find the radius as the average radius across all points
        rad = np.mean(np.sqrt((x - xc) ** 2 + (y - yc) ** 2))
        return xc, yc, rad

    def find_colinear_case_circle(self, x, y):
        """ Finds the best fitting circle when the points are colinear - simply finds the bounding circle
        :param x: The x coordinates of the marked points
        :param y: The y coordinates of the marked points
        :return xc: The x coordinate of the center of circle
                yc: The y coordinate of the center of circle
                rad: The radius of the circle
        """

        # The center is the middle between the maximal points
        xhalf = (np.max(x) - np.min(x)) / 2
        yhalf = (np.max(y) - np.min(y)) / 2
        xc = np.min(x) + xhalf
        yc = np.min(y) + yhalf

        # Radius is simply using pythagorean theorem
        rad = math.sqrt(xhalf * xhalf + yhalf * yhalf)
        return xc, yc, rad

    @pyqtSlot()
    def on_click(self):
        """ Function that gets called when the button is clicked. Generates the best fitting circle to selected points
        """

        # First identify all of the marked points
        [x, y] = self.find_marked_points()
        xc, yc, rad = -5, -5, 0

        if x.size > 2:      # If there are more than two points, we use least squares to solve
            try:
                [xc, yc, rad] = self.solve_least_squares_circle(x, y)
            except:         # If the points are colinear, then we use the simple colinear case to solve
                [xc, yc, rad] = self.find_colinear_case_circle(x, y)
        elif x.size > 1:  # If there are only two points, then we use the simple colinear case to solve
            [xc, yc, rad] = self.find_colinear_case_circle(x, y)

        # We set the center and edge points of the circle accordingly
        self.center = QPoint(xc + 5, yc + 5)
        self.edge = QPoint(xc + rad + 5, yc + 5)

        # If there is only one point, we draw a circle around that point
        if x.size == 1:
            self.center = QPoint(x[0] + 5, y[0] + 5)
            self.edge = QPoint(x[0] + 15, y[0] + 5)

        self.update()

    def resizeEvent(self, event):
        """ When window is resized, we want to make sure that our circle scales well too.
        :param event: The event object representing a window resize event
        """
        # Moves button to the updated location
        self.button.move(self.rect().width() / 2.0 - 50, self.rect().height() - 40)

        self.on_click()                             # Updates the circle location
        QMainWindow.resizeEvent(self, event)        # Makes sure that everything else is also handled well


if __name__ == "__main__":
    app = QApplication([])      # Create the application
    window = Window()           # Create the object
    sys.exit(app.exec_())       # Return when the window is closed
