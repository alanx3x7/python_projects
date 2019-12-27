# Alan Lai, 2019/11/02
# Neocis Coding Challenge

import math
import sys

import numpy as np
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    """ Main class for the application
    """

    def __init__(self):
        super().__init__()
        self.title = "Part 1"           # Title of the application

        self.top = 150                  # Location of application when it is launched
        self.left = 150                 # Location of application when it is launched
        self.width = 600                # Width of initial window
        self.height = 600               # Height of initial window
        self.num_xpoints = 20           # Number of points in x direction
        self.num_ypoints = 20           # Number of points in y direction

        self.setMouseTracking(True)     # Makes the application able to track the mouse
        self.clicked = False            # Starts off with an unclicked state

        self.center = QPoint(0, 0)      # Sets the center of the circle to be drawn to be 0
        self.edge = QPoint(0, 0)        # Sets the coordinate of the edge of a circle to be 0
        self.minimum_r = 0              # The minimum radius corresponding to smaller circle
        self.maximum_r = 0              # The maximum radius corresponding to larger circle

        self.init_window()              # Initialize the window

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
        size = self.size()                                  # Gets the size of current window

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

        # Draws the smaller red circle based on the minimum radius obtained previously
        qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        qp.drawEllipse(self.center, self.minimum_r, self.minimum_r)

        # Draws the larger red circle based on the maximum radius obtained previously
        qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        qp.drawEllipse(self.center, self.maximum_r, self.maximum_r)

    def mousePressEvent(self, event):
        """ Called when the mouse is pressed. Sets the location of click as center of circle
        :param event: The event object representing the click of the mouse
        """
        # Updates the center and edge as location of click
        self.center = event.pos()
        self.edge = event.pos()

        # Resets so that all points are the default gray colour
        self.colourList = [[Qt.gray] * self.num_xpoints for i in range(self.num_ypoints)]

        # Removes the red circles
        self.maximum_r = 0
        self.minimum_r = 0

        # Updates the display, and marks that clicking has commenced
        self.update()
        self.clicked = True

    def mouseMoveEvent(self, event):
        """ Called when mouse moves. This updates the edge of circle location if mouse is clicked
        :param event: The event object representing the movement of the mouse
        """
        # We only care if this is part of a click and drag movement
        if self.clicked:
            self.edge = event.pos()     # We update the position of the current edge
            self.update()               # Update so that the circle follows the cursor

    def mouseReleaseEvent(self, event):
        """ Called when mouse button is released. Marks nearby points as blue, and draws the red circles
        :param event: The event object representing the release of the mouse button
        """
        # First marks that the mouse button is no longer clicked
        self.clicked = False

        # Finds the distance from the center of the circle (marked when mouse clicked) and the current edge
        x_diff = self.edge.x() - self.center.x()
        y_diff = self.edge.y() - self.center.y()
        radius = math.sqrt(x_diff * x_diff + y_diff * y_diff)

        # Arbitrarily set values for curmin and curmax so they are overwritten
        curmin = max(self.size().width(), self.size().height())
        curmax = -1
        threshold = self.half_a_block()

        # Loops through all of the points
        for i in range(self.num_xpoints):
            for j in range(self.num_ypoints):

                # Finds the distance from the point to the center of the circle
                x_dist = self.pointLocation[i][j][0] - self.center.x()
                y_dist = self.pointLocation[i][j][1] - self.center.y()
                distance = math.sqrt(x_dist * x_dist + y_dist * y_dist)

                # If the distance is within a range from the edge of the circle
                if abs(distance - radius) < threshold:
                    self.colourList[i][j] = Qt.blue     # We change its colour to blue
                    if distance < curmin:               # We also update the minimum radius if it is the closest
                        curmin = distance               # point that we have marked as blue so far
                    if distance > curmax:               # We also update the maximum radius if it is the furthest
                        curmax = distance               # point that we have marked as blue so far

        # We adjust the radii so that they line within the center of points, and not at the top left edge
        self.minimum_r = curmin - 5
        self.maximum_r = curmax + 5
        self.update()

    def half_a_block(self):
        """ Scales the threshold for a point to be considered close to the circle and marked.
            Misnomer, since experimentally 40% of the corner to corner distance of the block works best
        :return: the threshold
        """
        size = self.rect()

        # Computes 40% of the corner to corner distance of a block for points
        x_width = ((size.width() - 100) / 21.0)
        y_width = ((size.width() - 100) / 21.0)
        return 0.4 * math.sqrt(x_width * x_width + y_width * y_width)

    def resizeEvent(self, event):
        """ When window is resized, we want to make sure that our circle scales well too.
        :param event: The event object representing a window resize event
        """
        self.update_circle()                    # Updates the circle location
        QMainWindow.resizeEvent(self, event)    # Makes sure that everything else is also handled well

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

    def update_circle(self):
        """ Updates the circle whenever we resize the window so that it is the same place wrt the marked points
        """

        # First identify all of the marked points
        [x, y] = self.find_marked_points()
        xc, yc, rad = -5, -5, 0

        if x.size > 2:      # If there are more than two points, we use least squares to solve
            try:
                [xc, yc, rad] = self.solve_least_squares_circle(x, y)
            except:         # If the points are colinear, then we use the simple colinear case to solve
                [xc, yc, rad] = self.find_colinear_case_circle(x, y)
        elif x.size > 1:    # If there are only two points, then we use the simple colinear case to solve
            [xc, yc, rad] = self.find_colinear_case_circle(x, y)

        # We set the center and edge points of the circle accordingly
        self.center = QPoint(xc + 5, yc + 5)
        self.edge = QPoint(xc + rad + 5, yc + 5)

        # If there is only one point, we draw a circle around that point
        if x.size == 1:
            self.center = QPoint(x[0] + 5, y[0] + 5)
            self.edge = QPoint(x[0] + 15, y[0] + 5)

        # We then find the maximum and minimum radii of the red circles
        [curmax, curmin] = self.find_max_min_radii()
        self.minimum_r = curmin - 5
        self.maximum_r = curmax + 5
        self.update()

    def find_max_min_radii(self):
        """ Finds the maximum and minimum radii given the marked points, to draw the red circles
        """
        # Arbitrarily set values for curmin and curmax so they are overwritten
        curmin = max(self.size().width(), self.size().height())
        curmax = -5

        # Loops through all of the points
        for i in range(self.num_xpoints):
            for j in range(self.num_ypoints):

                # We only care if the point is marked blue
                if self.colourList[i][j] == Qt.blue:

                    # Finds the distance from the point to the center of the circle
                    x_dist = self.pointLocation[i][j][0] - self.center.x()
                    y_dist = self.pointLocation[i][j][1] - self.center.y()
                    distance = math.sqrt(x_dist * x_dist + y_dist * y_dist)

                    if distance < curmin:       # If the distance is less than the current minimum radius
                        curmin = distance       # update curmin
                    if distance > curmax:       # If the distance is more than the current maximum radius
                        curmax = distance       # update curmax

        # If the minimum has not changed, we set it to the default of 5
        if curmin == max(self.size().width(), self.size().height()):
            curmin = 5

        return curmax, curmin


if __name__ == "__main__":
    app = QApplication([])      # Create the application
    window = Window()           # Create the object
    sys.exit(app.exec_())       # Return when the window is closed
