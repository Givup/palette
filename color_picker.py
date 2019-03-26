import pygame as pyg

from ui_elements import Slider
from maths import *

class ColorPicker:
    def __init__(self, pos):
        (_w, _h) = (256, 256)
        self.pos = [pos[0] - _w / 2, pos[1] - _h / 2]
        self.size = [_w, _h]
        self.r = 255
        self.g = 255
        self.b = 255
        self.show = False
        self.focus = False
        self.changed = True
        r_slider = Slider((255, 0, 0), (10, 120), (self.size[0] - 20, 30))
        g_slider = Slider((0, 255, 0), (10, 160), (self.size[0] - 20, 30))
        b_slider = Slider((0, 0, 255), (10, 200), (self.size[0] - 20, 30))
        self.sliders = (r_slider, g_slider, b_slider)

    def update(self, window_size):
        self.pos[0] = clamp(self.pos[0], 0, window_size[0] - self.size[0])
        self.pos[1] = clamp(self.pos[1], 0, window_size[1] - self.size[1])

    def render(self, surface, font):
        self.changed = False
        if self.show:
            pyg.draw.rect(surface, (127, 127, 127), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            pyg.draw.rect(surface, (50, 50, 50), (self.pos[0], self.pos[1], self.size[0], 30))
            pyg.draw.rect(surface, (130, 0, 0), (self.pos[0] + self.size[0] - 30, self.pos[1], 30, 30))
            pyg.draw.rect(surface, (50, 0, 0), (self.pos[0] + self.size[0] - 25, self.pos[1] + 13, 20, 5))

            pyg.draw.rect(surface, (self.r, self.g, self.b), (self.pos[0] + 60, self.pos[1] + 45, 50, 50))
            pyg.draw.rect(surface, (255, 255, 255), (self.pos[0] + 60, self.pos[1] + 45, 50, 50), 3)

            for slider in self.sliders:
                slider.render(surface, self.pos)

            rhex = f'{self.r:02X}'
            ghex = f'{self.g:02X}'
            bhex = f'{self.b:02X}'
            title = font.render("Color Picker #" + rhex + ghex + bhex, False, (255, 255, 255))
            surface.blit(title, (self.pos[0] + 5, self.pos[1] + 5))

            rsurf = font.render("R: " + str(int(255 * self.sliders[0].get_value())), False, (255, 255, 255))
            gsurf = font.render("G: " + str(int(255 * self.sliders[1].get_value())), False, (255, 255, 255))
            bsurf = font.render("B: " + str(int(255 * self.sliders[2].get_value())), False, (255, 255, 255))

            surface.blit(rsurf, (self.pos[0] + 125, self.pos[1] + 40))
            surface.blit(gsurf, (self.pos[0] + 125, self.pos[1] + 60))
            surface.blit(bsurf, (self.pos[0] + 125, self.pos[1] + 80))

    def mouse_pressed(self, mouse):
        if not self.show:
            return
        (mx, my) = mouse
        if mx >= self.pos[0] and mx <= self.pos[0] + self.size[0] and my >= self.pos[1] and my <= self.pos[1] + self.size[1]:
            self.focus = True
            if mx >= self.pos[0] + self.size[0] - 30 and mx <= self.pos[0] + self.size[0]:
                if my >= self.pos[1] and my <= self.pos[1] + 30:
                    self.show = False

    def mouse_drag(self, mouse, delta):
        consumed = False
        if not self.show:
            return consumed
        (mx, my) = mouse
        (dx, dy) = delta
        if mx >= self.pos[0] and mx <= self.pos[0] + self.size[0] and my >= self.pos[1] and my <= self.pos[1] + self.size[1]:
            consumed = True
            if not self.focus:
                return consumed
            if my >= self.pos[1] and my <= self.pos[1] + 30: # Dragging the top
                #self.pos[0] = clamp(self.pos[0] + dx, 0, SCREEN_W - self.size[0])
                #self.pos[1] = clamp(self.pos[1] + dy, 0, SCREEN_H - self.size[1])
                self.pos[0] = self.pos[0] + dx
                self.pos[1] = self.pos[1] + dy
                # TODO: Somehow give the window size
                pass
            else: # Sliders
                for slider in self.sliders:
                    if slider.mouse_drag(mouse, delta):
                        consumed = True
                        self.changed = True
                self.r = int(self.sliders[0].get_value() * 255)
                self.g = int(self.sliders[1].get_value() * 255)
                self.b = int(self.sliders[2].get_value() * 255)

        return consumed

    def mouse_released(self, mouse):
        self.focus = False

    def set_state(self, state):
        self.show = state
        
    def get_state(self):
        return self.show
    
    def show(self):
        self.show = True

    def hide(self):
        self.show = False

    def toggle(self):
        self.show = not self.show

    def set_color(self, color):
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        
        for i in range(3):
            self.sliders[i].value = color[i] / 255


    def get_color(self):
        return (self.r, self.g, self.b)
