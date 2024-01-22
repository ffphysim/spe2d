from libmath import *

class PhysicsObject:
    ### Represents a physics object in the world

    def __init__(self, world: 'World'):
        self.pos = o2()
        self.velocity = zero()
        self.acceleration = zero()
        self.mass = 1 # kg (this represents your mother)

        self.world = world
        self.chunk = None

    def add_force(self, force: vec2):
        self.acceleration.add(force / self.mass)
