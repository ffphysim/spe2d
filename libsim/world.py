from libmath import *
from libsim.object import *
from libsim.constants import *

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
        self.ticks = 0

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

    def get_or_create_chunk(self, pos: vec2):
        chunk: Chunk = self.chunks.get(pos)
        if chunk is None:
            chunk = self.create_chunk(pos)
        return chunk

    def update_containing_chunk(self, obj: PhysicsObject):
        oldChunk: Chunk = obj.chunk
        pos = obj.pos

        if oldChunk is None: oldChunk = self.origin_chunk
        oldChunkPos = oldChunk.pos

        # find next center chunk using position advance
        newChunkX = math.floor(pos.x / CHUNK_WIDTH)
        newChunkY = math.floor(pos.y / CHUNK_WIDTH)
        if newChunkX != oldChunkPos.x or newChunkY != oldChunkPos.y:
            newChunkPos = vec2(newChunkX, newChunkY)
            newChunk = self.get_or_create_chunk(newChunkPos)
            newChunk.objects.append(obj)
            obj.chunk = newChunk

            # add to surrounding chunks according to the
            # entities calculated chunk bounding box
            expand = obj.chunk_expand_bounds
            if False: # todo: expand is not None:
                obj.chunks.clear()
                exBB = bb2d(newChunkX - expand[0], newChunkY - expand[3],
                            newChunkX + expand[1], newChunkY + expand[2])

                # remove old chunks
                for oldExChunk in obj.chunks:
                    exPos: vec2 = oldExChunk.pos
                    if not exBB.contains_vec(exPos):
                        obj.chunks.discard(oldExChunk)
                        if obj in oldExChunk.objects:
                            oldExChunk.objects.remove(obj)

                #
            else:
                if obj in oldChunk.objects:
                    oldChunk.objects.remove(obj)

            obj.chunks.add(newChunk)

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

    def find_surrounding_chunks(self, obj: PhysicsObject):
        h = obj.relative_bb.h() // 16 + 2
        w = obj.relative_bb.w() // 16 + 2
        x = obj.pos.x // 16 - w / 2
        y = obj.pos.y // 16 - h / 2
        ax = 0
        ay = 0
        ls = []

        while ax < w:
            while ay < h:
                cx = x + ax
                cy = y + ay
                cp = vec2(cx, cy)
                chunk = self.chunks.get(cp)
                if chunk is not None:
                    ls.append(chunk)
                ay += 1
            ay = 0
            ax += 1

        return ls

    def update(self):
        to_remove = []

        # update all chunks per object
        for obj in self.objects:
            self.update_containing_chunk(obj)

            if obj.should_destroy_later:
                self.destroy_object(obj)

        # clean up unused chunks
        if self.ticks % 60 == 0:
            to_remove.clear()
            for chunk in self.chunks.values():
                if len(chunk.objects) == 0:
                    to_remove.append(chunk.pos)

            for pos in to_remove:
                self.chunks.pop(pos)

        self.ticks += 1