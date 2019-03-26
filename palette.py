import pygame as pyg

def create_default_palette():
    _palette = []
    for i in range(16):
        x = 10 + (i % 2) * 50
        y = 25 + 50 * int(i / 2)
        _color = (0, 0, 0)
        if i == 0:
            _color = (255, 255, 255)
        _palette.append(PaletteColor(i, _color, (x, y), (40, 40)))
    return _palette

class PaletteColor:
    def __init__(self, index, color, pos, size):
        self.index = index
        self.color = color
        self.pos = pos
        self.size = (30, 30)

    def is_inside(self, mouse):
        (mx, my) = mouse
        return mx >= self.pos[0] and mx <= self.pos[0] + self.size[0] and my >= self.pos[1] and my <= self.pos[1] + self.size[1]

    def render(self, surface, current_selection, current_secondary):
        pyg.draw.rect(surface, (self.color), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        if self.index == current_selection:
            pyg.draw.rect(surface, (255, 255, 255), (self.pos[0], self.pos[1], self.size[0], self.size[1]), 1)
        if self.index == current_secondary:
            pyg.draw.rect(surface, (255, 0, 255), (self.pos[0], self.pos[1], self.size[0], self.size[1]), 1)
