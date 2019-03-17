import pygame as pyg

SCREEN_W = 800
SCREEN_H = 600

TOOL_W = 125

pyg.init()
screen = pyg.display.set_mode((SCREEN_W, SCREEN_H))
edit_surface = pyg.Surface((SCREEN_W - TOOL_W, SCREEN_H))
pyg.display.set_caption("PixArt")
font = pyg.font.SysFont("Arial", 20)

running = True

MLEFT = 0
MRIGHT = 1
MMIDDLE = 2
mouse_clicked = [False, False, False]
mouse_down = [False, False, False]
mouse_released = [False, False, False]
mouse_dragging = False
mouse_drag = (0, 0)
mouse_last = (0, 0)
mouse_pos = (0, 0)
mouse_delta = [0, 0]
mouse_scroll = 0

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)

def load(filename):
    _file = open(filename, "r")
    
    _line = _file.readline()
    if not _line.startswith("PPA1"):
        print("Invalid file.\n")
        return

    _sizes = _file.readline().split()
    if len(_sizes) != 2:
        print("Invalid size!")
        return
    _w = int(_sizes[0])
    _h = int(_sizes[1])

    _palette_size = int(_file.readline())
    _palette = []

    for p in range(_palette_size):
        _line = _file.readline().split()
        _palette.append((int(_line[0]), int(_line[1]), int(_line[2])))
    
    _pixels = []
    _line  = _file.readline().split()
    for p in range(_w * _h):
        _pixels.append(int(_line[p]))

    return ImageEditWindow.from_data((_w, _h), _palette, _pixels)


def save(filename):
    file = open(filename, "w")
    file.write("PPA1\n")
    file.write(str(edit_window.get_w()) + " " + str(edit_window.get_h()) + "\n")
    file.write(str(len(edit_window.palette)) + "\n")
    for p in range(len(edit_window.palette)):
        file.write(str(edit_window.palette[p][0]) + " " + str(edit_window.palette[p][1]) + " " + str(edit_window.palette[p][2]) + "\n")
    for pix in edit_window.pixels:
        file.write(str(pix) + " ")

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

class ColorPicker:
    def __init__(self):
        self.pos = [SCREEN_W / 2 - 128, SCREEN_H / 2 - 128]
        self.size = [256, 256]
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

    def render(self, surface):
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
                self.pos[0] = clamp(self.pos[0] + dx, 0, SCREEN_W - self.size[0])
                self.pos[1] = clamp(self.pos[1] + dy, 0, SCREEN_H - self.size[1])
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

class ImageEditWindow:
    def __init__(self, size):
        self.size = size
        self.pixels = []
        self.palette_size = 16
        self.palette = []
        for _ in range(self.palette_size):
            self.palette.append((0, 0, 0))
        for i in range(self.size[0] * self.size[1]):
            self.pixels.append(0)

    def from_data(size, palette, pixels):
        _from = ImageEditWindow(size)
        _from.palette_size = len(palette)
        _from.palette = list(palette)
        _from.pixels = list(pixels)
        return _from

    def render(self, surface, offset, pixel_size):
        pyg.draw.rect(surface, (255, 255, 255), (offset[0], offset[1], pixel_size * self.size[0], pixel_size * self.size[1]))
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                pyg.draw.rect(surface, self.palette[self.pixels[x + y * self.size[0]]], (offset[0] + x * pixel_size, offset[1] + y * pixel_size, pixel_size, pixel_size))

    def set_pixel(self, pos, color):
        self.pixels[pos[0] + pos[1] * self.size[0]] = color

    def get_w(self):
        return self.size[0]

    def get_h(self):
        return self.size[1]

edit_window = ImageEditWindow((32, 32))
picker = ColorPicker()

palette = []
for i in range(16):
    x = 10 + (i % 2) * 50
    y = 25 + 50 * int(i / 2)
    palette.append(PaletteColor(i, (0, 0, 0), (x, y), (40, 40)))

selected_palette = 0
selected_secondary = 1

pix_x = 0
pix_y = 0
pix_size = 4

control = False

while running:
    for event in pyg.event.get():

        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                running = False
            if event.key == pyg.K_c:
                picker.toggle()
            if event.key == pyg.K_LCTRL:
                control = True
            if event.key == pyg.K_s:
                if control:
                    save("image.ppa")
            if event.key == pyg.K_l:
                if control:
                    edit_window = load("image.ppa")
                    for p in range(len(palette)):
                        palette[p].color = edit_window.palette[p]

            if event.key == pyg.K_n:
                if control:
                    edit_window = ImageEditWindow((32, 32))
                    for p in range(len(palette)):
                        palette[p].color = edit_window.palette[p]

        if event.type == pyg.KEYUP:
            if event.key == pyg.K_LCTRL:
                control = False


        if event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down[MLEFT] = True
                mouse_clicked[MLEFT] = True
            elif event.button == 2:
                mouse_down[MMIDDLE] = True
                mouse_clicked[MMIDDLE] = True
            elif event.button == 3:
                mouse_down[MRIGHT] = True
                mouse_clicked[MRIGHT] = True
            elif event.button == 4:
                mouse_scroll = 1
            elif event.button == 5:
                mouse_scroll = -1
                
        if event.type == pyg.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down[MLEFT] = False
                mouse_released[MLEFT] = True
            elif event.button == 2:
                mouse_down[MMIDDLE] = False
                mouse_released[MMIDDLE] = True
            elif event.button == 3:
                mouse_down[MRIGHT] = False
                mouse_released[MRIGHT] = True

        if event.type == pyg.MOUSEMOTION:
            mouse_dragging = False
            if True not in mouse_down:
                mouse_drag = event.pos
            else:
                mouse_dragging = True
            mouse_delta[0] = event.pos[0] - mouse_pos[0]
            mouse_delta[1] = event.pos[1] - mouse_pos[1]
            mouse_pos = event.pos
            mouse_last = (mouse_pos[0] - mouse_delta[0], mouse_pos[1] - mouse_delta[1])

    mouse_consumed = False

# Update

    if mouse_clicked[MLEFT]:
        picker.mouse_pressed(mouse_pos)
    elif mouse_released[MLEFT]:
        picker.mouse_released(mouse_pos)
    if mouse_down[MLEFT]:
        mouse_consumed = picker.mouse_drag(mouse_last, mouse_delta)

    # Editing the image
    if mouse_down.count(True) == 1 and not mouse_down[MMIDDLE] and not mouse_consumed and not picker.focus:
        (mx, my) = mouse_pos
        mx -= TOOL_W # Exclude the tool window area
        if mx > 0: # If we are in the editor window area
            if mx >= pix_x and mx < (pix_x + edit_window.get_w() * pix_size) and my >= pix_y and my < (pix_y + edit_window.get_h() * pix_size):
                # Pixel position (px, py)
                px = int((mx - pix_x) / pix_size)
                py = int((my - pix_y) / pix_size)
                if px >= 0 and px < edit_window.get_w() and py >= 0 and py < edit_window.get_h():
                    if mouse_down[MLEFT]:
                        edit_window.set_pixel((px, py), selected_palette)
                    elif mouse_down[MRIGHT]:
                        edit_window.set_pixel((px, py), selected_secondary)
    
    if mouse_down[MMIDDLE]:
        pix_x += mouse_delta[0]
        pix_y += mouse_delta[1]

    pix_size += mouse_scroll
    if pix_size < 1:
        pix_size = 1
    elif pix_size > 32:
        pix_size = 32

    if mouse_clicked[MLEFT]:
        for pc in palette:
            if pc.is_inside(mouse_pos):
                if selected_secondary == pc.index:
                    selected_secondary = selected_palette
                selected_palette = pc.index
                picker.set_color(palette[selected_palette].color)

    if mouse_clicked[MRIGHT]:
        for pc in palette:
            if pc.is_inside(mouse_pos):
                if selected_palette == pc.index:
                    selected_palette = selected_secondary
                selected_secondary = pc.index

    palette[selected_palette].color = picker.get_color()

# Render

    screen.fill((0, 0, 0))
    edit_surface.fill((200, 200, 200))
    
    pyg.draw.rect(screen, (170, 170, 170), (0, 0, 125, SCREEN_H))

    edit_window.render(edit_surface, (pix_x, pix_y), pix_size)

    screen.blit(edit_surface, (TOOL_W, 0))

    for (i, pc) in enumerate(palette):
        pc.render(screen, selected_palette, selected_secondary)
        edit_window.palette[i] = pc.color

    picker.render(screen)

    pyg.display.flip()

    mouse_clicked = [False, False, False]
    mouse_released = [False, False, False]
    mouse_scroll = 0
    mouse_delta = [0, 0]
