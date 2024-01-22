from libmath import *
from object import *

CHUNK_WIDTH: float = 20 # The width and height of a chunk

class Chunk:
    ### A chunk in a world used to optimize localized operations

    def __init__(self, world: 'World', pos: vec2):
        self.world = world
        self.pos = pos
        self.objects = [] # The objects contained by this chunk
        self.bb = bb2d(pos.x, pos.y, pos.x + CHUNK_WIDTH, pos.y + CHUNK_WIDTH)

        self.left  = None
        self.right = None
        self.up    = None
        self.down  = None

class World:
    ### A simulation world containing objects

    def __init__(self):
        self.objects = []
        self.chunks = {}

    def initialize_object(self, obj: PhysicsObject):
        obj.world = self
        obj.chunk =