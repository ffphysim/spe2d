import time

from libsim.world import *
from abc import abstractmethod

class Simulation:
    """
    A simulation works on a world object and updates each object in the world
    following the simulation rules.
    """

    def __init__(self, world):
        self.world = world

        # Common Simulation Utilities

        self.dt = 0.0 # The delta time to account for CPU speed in the simulation,
                      # in seconds.
        self.ticks = 0 # The amount of updates that have happened since the start of the simulation

    def invoke_timed_update(self, dt: float = None):
        t1 = time.time()

        if dt is not None:
            self.dt = dt

        # actually perform the update
        self.update(
            world=self.world,
            dt=self.dt
        )

        self.world.update()

        self.ticks += 1
        t2 = time.time()

        # update dt if it was not provided
        if dt is None:
            self.dt = t2 - t1 + 0.001
        return self.dt

    @abstractmethod
    def update(self, world: World, dt: float): pass

    def movement_pass(self):
        for obj in self.world.objects:
            obj.velocity.add(obj.acceleration * self.dt)
            obj.pos.add(obj.velocity * self.dt)