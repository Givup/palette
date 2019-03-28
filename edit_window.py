import pygame as pyg

class ImageEditWindow:
    def __init__(self, size):
        self.size = size
        self.pixels = []
        self.palette_size = 16
        self.palette = []
        for _ in range(self.palette_size):
            self.palette.append((255, 255, 255))
        for i in range(self.size[0] * self.size[1]):
            self.pixels.append(self.palette_size - 1)

    def from_data(size, palette, pixels):
        _from = ImageEditWindow(size)
        _from.palette_size = len(palette)
        _from.palette = list(palette)
        _from.pixels = list(pixels)
        return _from

    def render(self, surface, offset, pixel_size, show_grid):
        pyg.draw.rect(surface, (255, 255, 255), (offset[0], offset[1], pixel_size * self.size[0], pixel_size * self.size[1]))
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if pixel_size >= 8 and show_grid:
                    pyg.draw.rect(surface, (0, 0, 0), (offset[0] + x * pixel_size, offset[1] + y * pixel_size, pixel_size, pixel_size))
                    pyg.draw.rect(surface, self.palette[self.pixels[x + y * self.size[0]]], (offset[0] + x * pixel_size + 1, offset[1] + y * pixel_size + 1, pixel_size - 2, pixel_size - 2))
                else:
                    pyg.draw.rect(surface, self.palette[self.pixels[x + y * self.size[0]]], (offset[0] + x * pixel_size, offset[1] + y * pixel_size, pixel_size, pixel_size))

    def set_pixel(self, pos, color):
        self.pixels[pos[0] + pos[1] * self.size[0]] = color

    def get_pixel(self, pos):
        if pos[0] < 0 or pos[0] >= self.size[0] or pos[1] < 0 or pos[1] >= self.size[1]:
            return -1
        return self.pixels[pos[0] + pos[1] * self.size[0]]
        
    def get_w(self):
        return self.size[0]

    def get_h(self):
        return self.size[1]

    def get_size(self):
        return self.size

    def get_palette(self):
        _pal = list()
        for pc in self.palette:
            _pal.append(pc)
        return _pal

    def get_index_data(self):
        _data = list()
        for r in range(self.get_h()):
            _row = list()
            for c in range(self.get_w()):
                _row.append(self.pixels[c + r * self.get_h()])
            _data.append(list(_row))
        return _data

    def get_pixel_data(self):
        _data = list()
        _pal = self.get_palette()
        for r in range(self.get_h()):
            _row = list()
            for c in range(self.get_w()):
                _row.append(_pal[self.pixels[c + r * self.get_h()]])
            _data.append(list(_row))
        return _data
