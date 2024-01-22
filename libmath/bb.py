from libmath.vec import *
import math

class bb2d:
    ### Represents a 2D bounding box

    def __init__(self, x1, y1, x2, y2):
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x2, x1)
        self.y2 = max(y2, y1)

    def min(self):
        return vec2(self.x1, self.y1)

    def max(self):
        return vec2(self.x2, self.y2)

    def width(self):
        return abs(self.x2 - self.x1)

    def height(self):
        return abs(self.y2 - self.y1)

    def w(self):
        return abs(self.x2 - self.x1)

    def h(self):
        return abs(self.y2 - self.y1)

    def __repr__(self):
        return "bb(" + str(self.x1) + "," + str(self.y1) + " to " + str(self.x2) + "," + str(self.y2) + ")"