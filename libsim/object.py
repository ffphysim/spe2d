from typing import TypeVar

from libmath import *
from libsim.constants import *

S = TypeVar("S")

class PhysicsObject:
    ### Represents a physics object in the world

    def __init__(self, world: 'World'):
        self.pos = o2()
        self.velocity = zero()
        self.acceleration = zero()
        self.mass = 1 # kg (this represents your mother)

        self.world = world
        self.chunk = None
        self.chunks = set['Chunk']() # all chunks this entity might be in
        self.should_destroy_later = False

        self.relative_bb = None
        self.chunk_expand_bounds = None

        self.set_bb(bb2d(-2, -2, 2, 2))
        self.simulation_object: S = None

    def set_bb(self, bb: bb2d):
        self.relative_bb = bb

        if abs(bb.x1) <= CHUNK_WIDTH <= abs(bb.x2) and abs(bb.y1) <= CHUNK_WIDTH <= abs(bb.y2):
            self.chunk_expand_bounds = None
            return

        # calculate the amount of chunks to add surrounding the
        # object when its center/main chunk is recalculated
        self.chunk_expand_bounds = (
            (-bb.x1 // CHUNK_WIDTH),
            ( bb.x2 // CHUNK_WIDTH),
            (-bb.y1 // CHUNK_WIDTH),
            ( bb.y2 // CHUNK_WIDTH)
        )

    def destroy_later(self):
        self.should_destroy_later = True

    def add_force(self, force: vec2):
        self.acceleration.add(force.div_scalar(self.mass))

    def set_pos(self, vec: vec2) -> 'PhysicsObject':
        self.pos = vec
        return self

    def get_absolute_bb(self):
        x = self.pos.x
        y = self.pos.y
        return bb2d(self.relative_bb.x1 + x, self.relative_bb.y1 + y,
                    self.relative_bb.x2 + x, self.relative_bb.y2 + y)
