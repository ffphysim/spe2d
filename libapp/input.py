import pygame
from pygame.constants import *
from libmath import *

class InputManager:
    """
    Records and manages input on the mouse and keys.
    """

    def __init__(self):
        self.keys = {}    # keyboard keys
        self.buttons = {} # mouse buttons

        self.mouseX = 0
        self.mouseY = 0
        self.mouseDX = 0
        self.mouseDY = 0

        self.wheelDelta = 0

    def is_key_down(self, key):
        return key in self.keys

    def was_key_pressed(self, key):
        return self.keys.get(key) == 0

    def was_key_released(self, key):
        return self.keys.get(key) == -1

    def is_button_down(self, key):
        return key in self.buttons

    def was_button_pressed(self, key):
        return self.buttons.get(key) == 0

    def was_button_released(self, key):
        return self.buttons.get(key) == -1

    def tick(self, dt):
        for key in self.keys.copy():
            if self.keys[key] == -1:
                self.keys.pop(key)
            else:
                self.keys[key] += dt
        for btn in self.buttons.copy():
            if self.buttons[btn] == -1:
                self.buttons.pop(btn)
            else:
                self.buttons[btn] += dt

        self.mouseDX = 0
        self.mouseDY = 0
        self.wheelDelta = 0

    def register_key_down(self, key):
        self.keys[key] = 0

    def register_key_up(self, key):
        self.keys[key] = -1

    def register_button_down(self, key):
        self.buttons[key] = 0

    def register_button_up(self, key):
        self.buttons[key] = -1

    def register_mouse_move(self, posX, posY):
        self.mouseDX = posX - self.mouseX
        self.mouseDY = posY - self.mouseY
        self.mouseX = posX
        self.mouseY = posY

    def pygame_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.register_key_down(event.key)
        elif event.type == pygame.KEYUP:
            self.register_key_up(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.register_button_down(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.register_button_up(event.button)

        if event.type == pygame.MOUSEMOTION:
            self.register_mouse_move(event.pos[0], event.pos[1])
        if event.type == pygame.MOUSEWHEEL:
            self.wheelDelta = event.precise_y