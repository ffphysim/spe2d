import random
import sys

from libmath import *
from libsim import *
from libapp import *
import pygame

pygame.init()

##################################
# Rendering/Application (Debug mostly)
##################################

inputManager: InputManager = InputManager()

class CameraState:
    def __init__(self, screen: pygame.Surface):
        self.x = 0
        self.y = 0

        self.scale_x = 5
        self.scale_y = 5

        self.pan_sensitivity = 0.2
        self.zoom_sensitivity = 0.2

        self.running = False
        self.paused = False
        self.debug = True

        self.lastXCtrlPressed = None
        self.lastYCtrlPressed = None

        self.tick_dt = 0.0001

    def update_surface(self, screen: pygame.Surface):
        self.screen = screen
        self.w = screen.get_width()
        self.h = screen.get_height()

    def sx(self, x):
        return ((x - self.x) * self.scale_x) + (self.w / 2)

    def sy(self, y):
        return -((y - self.y) * self.scale_y) + (self.h / 2)

    def wx(self, sx):
        return (sx - self.w / 2) / self.scale_x + self.x

    def wy(self, sy):
        return -(sy - self.h / 2) / self.scale_x + self.y

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

    def has_x(self, x):
        return 0 <= x <= self.w

    def has_y(self, y):
        return 0 <= y <= self.h

    def has(self, vec: vec2):
        return 0 <= vec.x <= self.w and 0 <= vec.y <= self.h

    def has_rect(self, rect: pygame.Rect):
        x2 = rect.x + rect.w
        y2 = rect.y + rect.h

        return self.has_x(rect.x) and self.has_y(rect.y) or self.has_x(x2) and self.has_y(y2)

    def has_bb(self, bb: bb2d):
        return self.has_x(bb.x1) or self.has_y(bb.y1) or self.has_x(bb.x2) or self.has_y(bb.y2)

def fs(f: float):
    return str(round(f, 2))

def bb_to_rect(bb: bb2d):
    return pygame.Rect(bb.x1, bb.y1, bb.w(), bb.h())

def new_col(r, g, b, a=255) -> pygame.Color:
    return pygame.Color(r, g, b, a)

def new_rect(x, y, w, h) -> pygame.Rect:
    return pygame.Rect(x, y, w, h)

def render_text(surface: pygame.Surface, pos: tuple, s: str, font: pygame.font.Font, col: pygame.Color):
    text = font.render(s, True, col)
    surface.blit(text, pos)

font15 = pygame.font.SysFont("Arial Black", 15)
font8 = pygame.font.SysFont("Arial Black", 8)

ALIVE_RECT = bbcentered(o2(), vecsqr(100_000))

def render_debug(cam: CameraState, screen: pygame.Surface, world: World, sim: Simulation):
    worldMX = cam.wx(inputManager.mouseX)
    worldMY = cam.wy(inputManager.mouseY)

    rendered_chunks = 0
    rendered_objects = 0

    # Render chunk lines
    for chunk in world.chunks.values():
        bb = chunk.bb
        rect = cam.to_screen_rect(bb)

        if not cam.has_rect(rect): continue
        rendered_chunks += 1

        redness  = min(255, max(50, int(abs(chunk.pos.x * 10))))
        blueness = min(255, max(50, int(abs(chunk.pos.y * 10))))
        pygame.draw.rect(screen, new_col(redness, 0, blueness), rect, 1)

        if chunk.bb.contains(worldMX, worldMY):
            pygame.draw.rect(screen, new_col(redness, 0, blueness, 120), rect)

    kineticEnergy = 0

    # Render objects
    for obj in world.objects:
        instance_id = id(obj)

        bb = obj.get_absolute_bb()
        sbb = cam.to_screen_bb(bb)
        center = sbb.center().i()

        kineticEnergy += 0.5 * obj.mass * obj.velocity.magnitude() ** 2

        if not cam.has_bb(sbb): continue
        rendered_objects += 1

        brightness = (instance_id % 200) + 55
        col = new_col(brightness, brightness, brightness)

        pygame.draw.rect(screen, col, bb_to_rect(sbb), 1)
        pygame.draw.circle(screen, col, (center.x, center.y), int(sbb.w() / 2), int(max(2, min(5, obj.mass / 100)))) # mass = thick
        pygame.draw.circle(screen, col, (center.x, center.y), 2)
        render_text(screen, (center.x + 2, center.y + 2), "(" + fs(obj.pos.x) + "," + fs(obj.pos.y) + ")", font8, col)

        # render velocity and acceleration
        if False:
            damp = 100
            pygame.draw.line(screen, col, (center + obj.velocity.iy().normalize().mul_scalar(2)).tuple(), (center + obj.velocity.iy().mul_scalar(cam.scale_x).div_scalar(damp)).tuple(), 1)
            col.a = 200
            pygame.draw.line(screen, col, center.tuple(), (center + obj.acceleration.iy().mul_scalar(cam.scale_y).div_scalar(damp)).tuple(), 1)

    # Render Alive Rect
    sAliveRect = cam.to_screen_rect(ALIVE_RECT)
    col = new_col(255, 0, 0)
    pygame.draw.rect(screen, col, sAliveRect, 1)
    render_text(screen, (sAliveRect.x, sAliveRect.y - 12), str(ALIVE_RECT.w()), font8, col)

    if cam.lastXCtrlPressed is not None:
        pygame.draw.line(screen, new_col(0, 255, 0), (cam.sx(cam.lastXCtrlPressed), cam.sy(cam.lastYCtrlPressed)),
                         (cam.sx(worldMX), cam.sy(worldMY)), 4)

    # Render Cross
    CROSSHAIR_COLOR = new_col(220, 220, 220, 120)
    CROSSHAIR_HEIGHT = 8
    CROSSHAIR_WIDTH = 8
    cmx = math.ceil(CROSSHAIR_WIDTH / 2)
    cmy = math.ceil(CROSSHAIR_HEIGHT / 2)
    crosshairSurface = pygame.Surface((CROSSHAIR_WIDTH + 1, CROSSHAIR_HEIGHT + 1), pygame.SRCALPHA)
    pygame.draw.rect(crosshairSurface, CROSSHAIR_COLOR, new_rect(cmx, 0, 1, CROSSHAIR_HEIGHT + 1))
    pygame.draw.rect(crosshairSurface, CROSSHAIR_COLOR, new_rect(0, cmy, CROSSHAIR_WIDTH + 1, 1))
    screen.blit(crosshairSurface, (cam.w / 2 - CROSSHAIR_WIDTH / 2, cam.h / 2 - CROSSHAIR_HEIGHT / 2))

    render_text(screen, (10, 2), "dt: " + str(sim.dt) + ", ticks: " + str(sim.ticks) + " obj count: " + str(len(world.objects)) + ", chunks: " + str(
        len(world.chunks)),
                font15, new_col(255, 255, 255))
    render_text(screen, (10, 2 + 15 + 3),
                "cXY: (" + fs(cam.x) + "," + fs(cam.y) + "), zoom: " + fs(cam.scale_x) + ", mXY: (" + fs(
                    worldMX) + "," + fs(worldMY) + ")",
                font15, new_col(255, 255, 255))
    render_text(screen, (10, 2 + (15 + 3) * 2), "rendered chunks: " + str(rendered_chunks) + ", objs: " + str(rendered_objects),
                font15, new_col(255, 255, 255))
    render_text(screen, (10, 2 + (15 + 3) * 3), "Ekinetic: " + str(kineticEnergy),
                font15, new_col(240, 240, 240))

    if cam.paused:
        render_text(screen, (10, cam.h - 15 - 5), "Paused at " + str(sim.ticks) + " ticks", font15, new_col(255, 255, 255))

def new_user_object(sim: Simulation, pos: vec2, vel: vec2):
    obj = PhysicsObject(sim.world)
    # obj.mass = 5.9724E24
    obj.mass = 100000
    obj.velocity = vel
    obj.pos = pos
    sim.add_object(obj)
    obj.simulation_object.set_radius(20)
    return obj

def process_inputs(cam: CameraState, screen: pygame.Surface, world: World, sim: Simulation):
    worldMX = cam.wx(inputManager.mouseX)
    worldMY = cam.wy(inputManager.mouseY)

    # pausing
    if inputManager.was_key_pressed(K_SPACE):
        cam.paused = not cam.paused

    # panning
    if inputManager.is_button_down(BUTTON_MIDDLE) or inputManager.is_key_down(K_m):
        cam.x += -inputManager.mouseDX * cam.pan_sensitivity * 4 / cam.scale_x
        cam.y +=  inputManager.mouseDY * cam.pan_sensitivity * 4 / cam.scale_y

    # zooming
    if inputManager.wheelDelta != 0:
        cam.scale_x += inputManager.wheelDelta * cam.zoom_sensitivity * cam.scale_x
        cam.scale_y += inputManager.wheelDelta * cam.zoom_sensitivity * cam.scale_y
        cam.scale_x = max(0.001, cam.scale_x)
        cam.scale_y = max(0.001, cam.scale_y)

    # snapping
    if inputManager.is_key_down(K_LSHIFT) and inputManager.was_button_pressed(BUTTON_LEFT):
        cam.x = worldMX
        cam.y = worldMY

    # move to the farthest object or loaded chunk
    if inputManager.was_key_pressed(K_f):
        if len(world.objects) == 0:
            bestChunk = None
            bestDistance = 0
            o = o2()
            for chunk in world.chunks.values():
                d = chunk.pos.distance_sqr(o)
                if d >= bestDistance:
                    bestChunk = chunk
                    bestDistance = d

            cam.x = bestChunk.bb.center().x
            cam.y = bestChunk.bb.center().y
        else:
            bestObj = None
            bestDistance = 0
            o = o2()
            for obj in world.objects:
                d = obj.pos.distance_sqr(o)
                if d >= bestDistance:
                    bestObj = obj
                    bestDistance = d

            cam.x = bestObj.get_absolute_bb().center().x
            cam.y = bestObj.get_absolute_bb().center().y

    if inputManager.was_key_pressed(K_o):
        cam.x = 0
        cam.y = 0

    # adding objects
    if inputManager.was_button_pressed(BUTTON_LEFT) and inputManager.is_key_down(K_LCTRL):
        if cam.lastXCtrlPressed is None:
            cam.lastXCtrlPressed = worldMX
            cam.lastYCtrlPressed = worldMY
        else:
            cam.lastXCtrlPressed = None
            cam.lastYCtrlPressed = None

    if inputManager.is_button_down(BUTTON_RIGHT):
        if sim.ticks % 2 == 0:
            new_user_object(sim,
                            vec2(worldMX, worldMY),
                            zero())

    if inputManager.was_button_released(BUTTON_LEFT):
        if cam.lastXCtrlPressed is not None:
            new_user_object(sim,
                            vec2(cam.lastXCtrlPressed, cam.lastYCtrlPressed),
                            vec2(worldMX - cam.lastXCtrlPressed, worldMY - cam.lastYCtrlPressed).div_scalar(5))

            cam.lastXCtrlPressed = None
            cam.lastYCtrlPressed = None

    if inputManager.was_key_pressed(K_PERIOD):
        sim.invoke_timed_update(cam.tick_dt)
    if inputManager.is_key_down(K_COMMA):
        sim.invoke_timed_update(cam.tick_dt)
    if inputManager.is_key_down(K_UP):
        cam.tick_dt += 0.001
        render_text(cam.screen, (0, 0), "step dt: " + str(cam.tick_dt), font8, new_col(255, 255, 255))
    if inputManager.is_key_down(K_DOWN):
        cam.tick_dt -= 0.001
        render_text(cam.screen, (0, 0), "step dt: " + str(cam.tick_dt), font8, new_col(255, 255, 255))

def render_world_and_simulation(cam: CameraState, screen: pygame.Surface, world: World, sim: Simulation):
    if cam.debug:
        render_debug(cam, screen, world, sim)

    process_inputs(cam, screen, world, sim)

##################################
# Simulation
##################################

G = 6.6743 * 200

class MySimulationObject(SimulationObject):
    def __init__(self, obj):
        super().__init__(obj)

        self.radius = 0
        self.collision_dampening = 0.12

    def set_radius(self, radius):
        self.radius = radius
        self.obj.set_bb(bb2d(-radius * 2, -radius * 2, radius * 2, radius * 2))

class MySimulation(Simulation):
    def apply_gravity(self, obj: PhysicsObject, objOther: PhysicsObject):
        d = obj.pos.distance_sqr(objOther.pos)
        if d == 0: return

        mag = G * ((obj.mass * objOther.mass) / d) # calculate the force
        obj.add_force(obj.pos.dir(objOther.pos).mul_scalar(mag))

    def find_collision(self, a: MySimulationObject, b: MySimulationObject) -> [vec2, vec2]:
        rA = a.radius
        rB = b.radius
        rd = rA + rB
        posA = a.obj.pos
        posB = b.obj.pos.clone()

        # check for collision using radius equation
        if posA.distance(posB) / 2 <= rd:
            dir = posA.dir(posB)
            point = dir.mul_scalar(rA)
            return point, dir, None  # todo: find point/normal of collision

        # check for collision in the future using radius equation
        # posB.add(b.obj.velocity * self.dt)
        # if posA.distance(posB) / 2 <= rd:
        #     dir = posA.dir(posB)
        #     point = dir.mul_scalar(rA)
        #     dv = dir.clone().mul_scalar((rA + rB) * 4)
        #     fixedPos = posB.add(-dv) # position of obj b so it barely touches the surface of obj a
        #     return point, dir, fixedPos

        return None, None, None


    def solve_collisions(self, a: MySimulationObject, b: MySimulationObject):
        point, normal, predictedPos = self.find_collision(a, b)
        if point is not None:
            bObj: PhysicsObject = b.obj
            if predictedPos is not None:
                bObj.pos = predictedPos

            # apply forces of collision in the right direction
            forceMagnitude = bObj.mass * (bObj.velocity.magnitude() * self.dt) * b.collision_dampening

            a.obj.add_force(-normal.clone().mul_scalar(forceMagnitude))
            b.obj.add_force( normal.clone().mul_scalar(forceMagnitude))
            a.obj.velocity = zero()
            b.obj.velocity = zero()

    def update(self, world: World, dt: float):
        # apply gravity
        for obj in world.objects:
            obj.acceleration = zero()

            # accurate gravity calculation
            for objB in world.objects: self.apply_gravity(obj, objB)

            if not ALIVE_RECT.contains_vec(obj.pos):
                obj.acceleration.neg()
                obj.velocity.neg()
                if obj.pos.distance(ALIVE_RECT.center()) > ALIVE_RECT.w() * 1.5:
                    obj.destroy_later()

        # solve collisions
        for obj in world.objects:
            # for chunk in obj.chunks:
            for objOther in world.objects:
                if obj != objOther:
                    self.solve_collisions(obj.simulation_object, objOther.simulation_object)

        self.movement_pass()

    def init_object(self, obj: PhysicsObject):
        obj.simulation_object = MySimulationObject(obj)
        obj.simulation_object.set_radius(100)


##################################
# Application
##################################

def randomize_alive_rect(sim: MySimulation):
    for i in range(0, 50):
        x = random.randrange(ALIVE_RECT.x1, ALIVE_RECT.x2)
        y = random.randrange(ALIVE_RECT.y1, ALIVE_RECT.y2)
        # VELR = 3000
        # vx = random.randrange(-VELR, VELR)
        # vy = random.randrange(-VELR, VELR)
        m = random.randrange(100, 200000)
        o = PhysicsObject(world)
        o.set_pos(vec2(x, y))
        # o.velocity = vec2(vx, vy)
        o.mass = m
        sim.add_object(o)
        o.simulation_object.set_radius(m / 10000)

def run_app(argv):

    ##########################################
    # Simulation Setup
    ##########################################

    # Create world and simulation
    world: World = World()
    simulation: MySimulation = MySimulation(world)

    singularity = PhysicsObject(world)
    singularity.mass = 1988500E24
    singularity.set_bb(bb2d(-200, -200, 200, 200))
    # simulation.add_object(singularity)
    # singularity.simulation_object.set_radius(20000)

    randomize_alive_rect(simulation)

    ##########################################
    # Initialization
    ##########################################

    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("spe2d")

    cam: CameraState = CameraState(screen)
    cam.running = True
    cam.scale_x = 0.1
    cam.scale_y = 0.1

    dt: float = 0
    FPS = 60

    while cam.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cam.running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            inputManager.pygame_event(event)

        if not cam.paused:
            SUBSTEPS = 1
            udt = dt / SUBSTEPS
            for i in range(0, SUBSTEPS):
                # perform simulation update
                simulation.invoke_timed_update(udt)
                pass

        screen.fill("black")
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cam.update_surface(surface)
        render_world_and_simulation(cam, surface, world, simulation)
        screen.blit(surface, (0, 0))

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000.0
        inputManager.tick(dt)

    pygame.quit()

if __name__ == "__main__":
    run_app(sys.argv)