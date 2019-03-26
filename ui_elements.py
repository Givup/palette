import pygame as pyg

from maths import *

class Button:
    def __init__(self, pos, size = (0, 0), text = None, image = None, assets = None):
        self.pos = pos
        if image != None:
            self.size = assets.get_image(image).get_size()
        else:
            self.size = size
        self.text = text
        self.image = image

        self.bounds = (pos, self.size)

        if text != None:
            self.text_surface = None
            self.text_size = None

        self.state = 0
        self.changed_state = 0

    def toggle(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0
        self.changed_state = 1

    def mouse_held(self, mouse):
        (mx, my) = mouse

    def mouse_released(self, mouse):
        # If mouse is released on top of this button
        if is_inside(mouse, self.bounds):
            self.toggle()

    def is_down(self):
        return self.state == 1

    def render(self, assets, surface, font):
        self.changed_state = 0
        if self.state == 0:
            pyg.draw.rect(surface, (200, 200, 200), self.bounds)
        if self.state == 1:
            pyg.draw.rect(surface, (125, 125, 125), self.bounds)    
        if self.text != None:
            if self.text_surface == None:
                self.text_surface = font.render(self.text, False, (0, 0, 0))
                self.text_size = font.size(self.text)
            text_off_x = self.pos[0] + self.size[0] / 2 - self.text_size[0] / 2
            text_off_y = self.pos[1] + self.size[1] / 2 - self.text_size[1] / 2
            surface.blit(self.text_surface, (text_off_x, text_off_y))
        elif self.image != None:
            if isinstance(self.image, list):
                _image = assets.get_image(self.image)
                surface.blit(_image, self.pos)
            else:
                _image = assets.get_image(self.image[self.state])
                surface.blit(_image, self.pos)
                    
class Slider:
    def __init__(self, color, pos, size):
        self.pos = pos
        self.offset = (0, 0)
        self.color = color
        self.size = size
        self.value = 1

    def render(self, surface, offset):
        self.offset = offset
        pos = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])
        pyg.draw.rect(surface, (self.color), (pos[0], pos[1], self.size[0], self.size[1]))
        pyg.draw.rect(surface, (255, 255, 255), (pos[0], pos[1], self.size[0], self.size[1]), 1)
        vx = self.value * (self.size[0])
        pyg.draw.rect(surface, (255, 255, 255), (pos[0] - 5 + vx, pos[1], 10, self.size[1]))

    def mouse_drag(self, mouse, delta):
        (mx, my) = mouse
        (dx, dy) = delta
        (x, y) = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])

        if mx >= x and mx <= x + self.size[0] and my >= y and my <= y + self.size[1]:
            self.value = (mx - x) / self.size[0]
            self.value = clamp(self.value, 0, 1)
            return True
        return False

    def get_value(self):
        return self.value

