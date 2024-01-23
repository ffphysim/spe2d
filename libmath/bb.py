from libmath.vec import *
import math

def bbcentered(center: vec2, size: vec2):
    return bb2d(center.x - size.x / 2, center.y - size.y / 2, center.x + size.x / 2, center.y + size.y / 2)

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

    def center(self) -> vec2:
        return vec2((self.x2 + self.x1) / 2, (self.y2 + self.y1) / 2)

    def contains(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def contains_vec(self, vec: vec2):
        return self.contains(vec.x, vec.y)

    def __contains__(self, item):
        if item is vec2:
            return self.contains(item.x, item.y)

    def __repr__(self):
        return "bb(" + str(self.x1) + "," + str(self.y1) + " to " + str(self.x2) + "," + str(self.y2) + ")"