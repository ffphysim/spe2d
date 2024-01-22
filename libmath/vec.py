import math

def o2():
    return vec2(0, 0)

def origin2():
    return vec2(0, 0)

def zero():
    return vec2(0, 0)

class vec2:
    ### A two-dimensional X, Y vector

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def clone(self):
        return vec2(self.x, self.y)

    def neg(self) -> 'vec2':
        self.x = -self.x
        self.y = -self.y
        return self

    def __neg__(self):
        return vec2(-self.x, -self.y)

    def add(self, other) -> 'vec2':
        self.x += other.x
        self.y += other.y
        return self

    def sub(self, other) -> 'vec2':
        self.x -= other.x
        self.y -= other.y
        return self

    def mul(self, other) -> 'vec2':
        self.x *= other.x
        self.y *= other.y
        return self

    def div(self, other) -> 'vec2':
        self.x /= other.x
        self.y /= other.y
        return self

    def __iadd__(self, other): return self.add(other)
    def __isub__(self, other): return self.sub(other)
    def __imul__(self, other): return self.mul(other)
    def __idiv__(self, other): return self.div(other)

    def __add__(self, other: 'vec2'):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'vec2'):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: 'vec2'):
        return vec2(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: 'vec2'):
        return vec2(self.x / other.x, self.y / other.y)

    def __mul__(self, other: int):
        return vec2(self.x * other, self.y * other)

    def __truediv__(self, other: int):
        return vec2(self.x / other, self.y / other)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def magnitude_sqr(self):
        return self.x * self.x + self.y * self.y

    def distance(self, other: 'vec2'):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx * dx + dy * dy)

    def distance_sqr(self, other: 'vec2'):
        dx = other.x - self.x
        dy = other.y - self.y
        return dx * dx + dy * dy

    def normalized(self) -> 'vec2':
        m = 1 / math.sqrt(self.x * self.x + self.y * self.y)
        self.x = self.x * m
        self.y = self.y * m
        return self

    def normalize(self):
        m = 1 / math.sqrt(self.x * self.x + self.y * self.y)
        return vec2(self.x * m, self.y * m)

    def dot(self, other: 'vec2'):
        return (self.x * other.x) + (self.y * other.y)

    def swap(self) -> 'vec2':
        tmp = self.x
        self.x = self.y
        self.y = tmp
        return self

    def yx(self):
        return vec2(self.y, self.x)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"