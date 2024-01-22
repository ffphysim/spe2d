import sys

from libmath import *
from libsim import *
import pygame

##################################
# Rendering (Debug mostly)
##################################

class CameraState:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.w = screen.get_width()
        self.h = screen.get_height()
        self.x = 0
        self.y = 0
        self.scale_x = 5
        self.scale_y = 5
        self.running = False

    def sx(self, x):
        return ((x - self.x) * self.scale_x) + (self.w / 2)

    def sy(self, y):
        return -((y - self.y) * self.scale_y) + (self.h / 2)

    def to_screen_vec(self, vec: vec2):
        return vec2(self.sx(vec.x), self.sy(vec.y))

    def to_screen_bb(self, bb: bb2d):
        return bb2d(
            self.sx(bb.x1),
            self.sy(bb.y1),
            self.sx(bb.x2),
            self.sy(bb.y2)
        )

    def to_screen_rect(self, bb: bb2d) -> pygame.Rect:
        return bb_to_rect(self.to_screen_bb(bb))

def bb_to_rect(bb: bb2d):
    return pygame.Rect(bb.x1, bb.y1, bb.w(), bb.h())

# from: https://stackoverflow.com/questions/61951026/pygame-drawing-a-border-of-a-rectangle
def create_rect(width, height, border, color, border_color):
    surf = pygame.Surface((width+border*2, height+border*2), pygame.SRCALPHA)
    if color is not None:
        pygame.draw.rect(surf, color, (border, border, width, height), 0)
    for i in range(1, border):
        pygame.draw.rect(surf, border_color, (border-i, border-i, width+i, height+i), 1)
    return surf

def new_col(r, g, b) -> pygame.Color:
    return pygame.Color(r, g, b)

def new_rect(x, y, w, h) -> pygame.Rect:
    return pygame.Rect(x, y, w, h)

def render_text(surface: pygame.Surface, pos: tuple[int, int], s: str, font: pygame.font.Font, col: pygame.Color):
    text = font.render(s, True, col)
    surface.blit(text, pos)

def poll_events(cam: CameraState):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cam.running = False

def render_world_and_simulation(cam: CameraState, screen: pygame.Surface, world: World, sim: Simulation):
    font = pygame.font.SysFont("Arial Black", 15)
    render_text(screen, (10, 2), "dt: " + str(sim.dt) + ", obj count: " + str(len(world.objects)), font, new_col(255, 255, 255))

    screen.fill(0xffffff, pygame.Rect(640, 880, 200, 200))

    # Render chunk lines
    for chunk in world.chunks.values():
        redness = max(0, 150 - int(chunk.pos.distance(o2()) * 10))
        pygame.draw.rect(screen, new_col(redness, 0, 0), cam.to_screen_rect(chunk.bb), 2)
        # screen.fill(pygame.Color(redness, 0, 0), cam.to_screen_rect(chunk.bb))

    # Render objects
    for obj in world.objects:
        pygame.draw.rect(screen, new_col(255, 255, 255), cam.to_screen_rect(obj.get_absolute_bb()))

##################################
# Simulation
##################################

class MySimulation(Simulation):
    def update(self, world: World, dt: float):
        for obj in world.objects:
            if abs(obj.velocity.y) < 100: # terminal velocity when falling
                gravity = vec2(0, -9.8)
                obj.acceleration.add(gravity)

            obj.velocity.add(obj.acceleration * dt)
            obj.pos.add(obj.velocity * dt)

            if obj.pos.y < -100000:
                obj.destroy_later()


##################################
# Application
##################################

def run_app(argv):

    ##########################################
    # Simulation Setup
    ##########################################

    # Create world and simulation
    world: World = World()
    simulation: MySimulation = MySimulation(world)

    for x in range(4, 100, 10):
        world.initialize_object(PhysicsObject(world).set_pos(vec2(x, 0)))

    ##########################################
    # Initialization
    ##########################################

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    cam: CameraState = CameraState(screen)
    cam.running = True

    while cam.running:
        poll_events(cam)

        # perform simulation update
        simulation.invoke_timed_update()

        screen.fill("black")
        render_world_and_simulation(cam, screen, world, simulation)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_app(sys.argv)