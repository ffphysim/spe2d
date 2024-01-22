from libmath import *
from libsim.object import *

CHUNK_WIDTH: float = 20 # The width and height of a chunk

class Chunk:
    """
    A chunk in a world used to optimize localized operations
    """

    def __init__(self, world: 'World', pos: vec2):
        self.world = world
        self.pos: vec2 = pos
        self.objects = [] # The objects contained by this chunk
        wx = pos.x * CHUNK_WIDTH
        wy = pos.y * CHUNK_WIDTH
        self.bb = bb2d(wx, wy, wx + CHUNK_WIDTH, wy + CHUNK_WIDTH)

        self.left  = None
        self.right = None
        self.up    = None
        self.down  = None

class World:
    """
    A simulation world containing objects
    """

    def __init__(self):
        self.objects: list[PhysicsObject] = []
        self.chunks: dict[vec2, Chunk] = {}
        self.origin_chunk: Chunk = self.create_chunk(o2())

    def create_chunk(self, pos: vec2) -> Chunk:
        newChunk = Chunk(self, pos)
        self.chunks[pos] = newChunk
        pos = pos.clone()

        # update surrounding chunks if existent
        otherChunk: Chunk
        otherChunk = self.chunks.get(pos.addc(-1, 0)) # 0 - 1 = -1 | left
        if otherChunk: otherChunk.right = newChunk; newChunk.left = otherChunk
        otherChunk = self.chunks.get(pos.addc( 2, 0)) # -1 + 2 = 1 | right
        if otherChunk: otherChunk.left = newChunk; newChunk.right = otherChunk
        otherChunk = self.chunks.get(pos.addc(-1, 1)) # 0 + 1 = 1 | up | also moves back to the middle
        if otherChunk: otherChunk.down = newChunk; newChunk.up = otherChunk
        otherChunk = self.chunks.get(pos.addc(-2, 0)) # 1 - 2 = -1 | down
        if otherChunk: otherChunk.up = newChunk; newChunk.down = otherChunk

        return newChunk

    def update_containing_chunk(self, obj: PhysicsObject):
        oldChunk: Chunk = obj.chunk
        pos = obj.pos

        if oldChunk is None: oldChunk = self.origin_chunk
        oldChunkPos = oldChunk.pos

        # find next chunk using position advance
        newChunkX = math.floor(pos.x / CHUNK_WIDTH)
        newChunkY = math.floor(pos.y / CHUNK_WIDTH)
        if newChunkX != oldChunkPos.x or newChunkY != oldChunkPos.y:
            if obj in oldChunk.objects:
                oldChunk.objects.remove(obj)
            newChunkPos = vec2(newChunkX, newChunkY)
            newChunk: Chunk = self.chunks.get(newChunkPos)
            if newChunk is None:
                newChunk = self.create_chunk(newChunkPos)
            newChunk.objects.append(obj)
            obj.chunk = newChunk

    def initialize_object(self, obj: PhysicsObject) -> PhysicsObject:
        obj.world = self
        self.objects.append(obj)
        self.update_containing_chunk(obj)
        return obj

    def destroy_object(self, obj: PhysicsObject):
        obj.world = None
        if obj in self.objects:
            self.objects.remove(obj)
        if obj.chunk is not None:
            chunk: Chunk = obj.chunk
            if obj in chunk.objects:
                chunk.objects.remove(obj)

    def update(self):
        # update all chunks per object
        for obj in self.objects:
            self.update_containing_chunk(obj)

            if obj.should_destroy_later:
                self.destroy_object(obj)