from libmath import *

class PhysicsObject:
    ### Represents a physics object in the world

    def __init__(self, world: 'World'):
        self.pos = o2()
        self.velocity = zero()
        self.acceleration = zero()
        self.mass = 1 # kg (this represents your mother)
        self.relative_bb = bb2d(-2, -2, 2, 2)

        self.world = world
        self.chunk = None
        self.should_destroy_later = False

    def destroy_later(self):
        self.should_destroy_later = True

    def add_force(self, force: vec2):
        self.acceleration.add(force / self.mass)

    def set_pos(self, vec: vec2) -> 'PhysicsObject':
        self.pos = vec
        return self

    def get_absolute_bb(self):
        x = self.pos.x
        y = self.pos.y
        return bb2d(self.relative_bb.x1 + x, self.relative_bb.y1 + y,
                    self.relative_bb.x2 + x, self.relative_bb.y2 + y)
