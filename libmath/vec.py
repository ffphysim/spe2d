import math

def o2():
    return vec2(0, 0)

def origin2():
    return vec2(0, 0)

def zero():
    return vec2(0, 0)

def vecsqr(v):
    return vec2(v, v)

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

    def add(self, other: 'vec2') -> 'vec2':
        self.x += other.x
        self.y += other.y
        return self

    def sub(self, other: 'vec2') -> 'vec2':
        self.x -= other.x
        self.y -= other.y
        return self

    def mul(self, other: 'vec2') -> 'vec2':
        self.x *= other.x
        self.y *= other.y
        return self

    def div(self, other: 'vec2') -> 'vec2':
        self.x /= other.x
        self.y /= other.y
        return self

    def addc(self, ox, oy) -> 'vec2':
        self.x += ox
        self.y += oy
        return self

    def subc(self, ox, oy) -> 'vec2':
        self.x -= ox
        self.y -= oy
        return self

    def mulc(self, ox, oy) -> 'vec2':
        self.x *= ox
        self.y *= oy
        return self

    def divc(self, ox, oy) -> 'vec2':
        self.x /= ox
        self.y /= oy
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

    def __mul__(self, other: float):
        return vec2(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return vec2(self.x / other, self.y / other)

    def mul_scalar(self, other: float) -> 'vec2':
        self.x *= other
        self.y *= other
        return self

    def div_scalar(self, other: float):
        self.x /= other
        self.y /= other
        return self

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

    def normalize(self) -> 'vec2':
        mag = self.magnitude()
        if mag == 0: return vec2(0, 0)
        m = 1 / mag
        self.x = self.x * m
        self.y = self.y * m
        return self

    def normalized(self):
        mag = math.sqrt(self.x * self.x + self.y * self.y)
        if mag == 0: return vec2(0, 0)
        m = 1 / mag
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

    def intdiv(self, scalar: int):
        return vec2(int(self.x) / scalar, int(self.y) / scalar)

    def left(self, a: float = 1):
        return vec2(self.x - a, self.y)

    def right(self, a: float = 1):
        return vec2(self.x + a, self.y)

    def up(self, a: float = 1):
        return vec2(self.x, self.y + a)

    def down(self, a: float = 1):
        return vec2(self.x, self.y - a)

    def __floor__(self):
        return vec2(math.floor(self.x), math.floor(self.y))

    def __round__(self, n=None):
        return vec2(round(self.x, n), round(self.y, n))

    def __int__(self):
        return vec2(int(self.x), int(self.y))

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __hash__(self):
        return hash(self.x) + 31 * hash(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def dir(self, other: 'vec2'):
        return (other - self).normalize()

    def tuple(self):
        return self.x, self.y

    def iy(self):
        return vec2(self.x, -self.y)

    def i(self):
        return vec2(int(self.x), int(self.y))