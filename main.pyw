import os

'''
Private imports
'''

from assets import Assets
from image_io import *
from ui_elements import *
from palette import *
from color_picker import *

import pygame as pyg

import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from maths import *

'''
Controls:

Ctrl-L: Load image.ppa
Ctrl-S: Save image.ppa
Ctrl-N: Create new image (32x32 by default)
Ctrl-E: Export image (PNG)
Ctrl-I: Import image (PNG, doesn't always work)
Ctrl-R: Reload assets (icons)

Scrollwheel: Scale pixels / Zoom
Mouse Left / Right: Paint

X: Swap main and secondary color
C: Toggle color picker visibility
G: Toggle grid visibility

B: Set tool to "Brush"
F: Set tool to "Fill"

Escape: Quit application
'''

tk_root = tk.Tk()
tk_root.withdraw()

SCREEN_W = 800
SCREEN_H = 600

TOOL_W = 125

pyg.init()
screen = pyg.display.set_mode((SCREEN_W, SCREEN_H), pyg.RESIZABLE)
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

def ask_width_height():
    _w = simpledialog.askinteger(title="New width", prompt="Width")
    _h = simpledialog.askinteger(title="New height", prompt="Height")
    return (_w, _h)

assets = Assets()

edit_window = ImageEditWindow((32, 32))
picker = ColorPicker((SCREEN_W / 2, SCREEN_H / 2))

palette = create_default_palette()

selected_palette = 0
selected_secondary = 1

picker.set_color(palette[selected_palette].color)

pix_size = 4
pix_x = (SCREEN_W - TOOL_W) / 2 - edit_window.size[0] * pix_size / 2
pix_y = SCREEN_H / 2 - edit_window.size[1] * pix_size / 2

control = False

grid_button = Button([4, SCREEN_H - 50], image = ("grid", "grid_active"), assets = assets)
wheel_button = Button([40, SCREEN_H - 50], image = ("color_wheel", "color_wheel_active"), assets = assets)
fill_button = Button([76, SCREEN_H - 50], image = ("fill_tool", "fill_tool_active"), assets = assets)

buttons = (grid_button, wheel_button, fill_button)

tool = "brush"

while running:
    for event in pyg.event.get():

        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.VIDEORESIZE:
            if event.w < 800 or event.h < 600:
                screen = pyg.display.set_mode((max(event.w, 800),max(event.h, 600)), pyg.RESIZABLE)
            else:
                print((event.w, event.h))
                SCREEN_W = event.w
                SCREEN_H = event.h
                screen = pyg.display.set_mode((event.w, event.h), pyg.RESIZABLE)
                edit_surface = pyg.Surface((SCREEN_W, SCREEN_H))
                for button in buttons:
                    button.pos[1] = SCREEN_H - 50

        if event.type == pyg.KEYDOWN:

            if event.key == pyg.K_ESCAPE:
                running = False

            if event.key == pyg.K_c:
                wheel_button.toggle()

            if event.key == pyg.K_LCTRL:
                control = True

            if event.key == pyg.K_s:
                if control:
                    save(edit_window)

            if event.key == pyg.K_l:
                if control:
                    new_image = load()
                    if new_image != None:
                        edit_window = new_image
                        for p in range(len(palette)):
                            palette[p].color = edit_window.palette[p]

            if event.key == pyg.K_e:
                if control:
                    export_png(edit_window)

            if event.key == pyg.K_i:
                if control:
                    new_image = import_png()
                    if new_image != None:
                        edit_window = new_image
                        for p in range(len(palette)):
                            palette[p].color = edit_window.palette[p]
                        selected_palette = 0
                        selected_secondary = 1
                        picker.set_color(palette[selected_palette].color)

            if event.key == pyg.K_f:
              if not control:
                fill_button.toggle()
                if fill_button.is_down():
                    tool = "fill"
                else:
                    tool = "brush"
                
            if event.key == pyg.K_b:
              if not control:
                tool = "brush"
                fill_button.state = 0
                        
            if event.key == pyg.K_r:
                if control:
                    load_assets()

            if event.key == pyg.K_n:
                if control:
                    (_w, _h) = ask_width_height()
                    if _w > 0 and _h > 0:
                        edit_window = ImageEditWindow((_w, _h))
                        palette = create_default_palette()
                        selected_palette = 0
                        selected_secondary = 1
                        picker.set_color(palette[selected_palette].color)
                        for p in range(len(palette)):
                            edit_window.palette[p] = palette[p].color

            if event.key == pyg.K_x:
                _temp_palette = selected_palette
                selected_palette = selected_secondary
                selected_secondary = _temp_palette
                picker.set_color(palette[selected_palette].color)

            if event.key == pyg.K_g:
                grid_button.toggle()

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

# Update

    mouse_consumed = False

    picker.update((SCREEN_W, SCREEN_H))

    if mouse_clicked[MLEFT]:
        picker.mouse_pressed(mouse_pos)
    elif mouse_released[MLEFT]:
        picker.mouse_released(mouse_pos)
        for button in buttons:
            button.mouse_released(mouse_pos)
    if mouse_down[MLEFT]:
        mouse_consumed = picker.mouse_drag(mouse_last, mouse_delta)

    # Next block must be after mouse clicks and releases
    # Force color wheel down if it is closed with the '-' sign on the picker itself
    if not picker.show and not wheel_button.changed_state == 1 and wheel_button.state == 1:
        wheel_button.state = 0
    picker.set_state(wheel_button.is_down())
    
    # Editing the image, used with brush tool
    if mouse_down.count(True) == 1 and not mouse_down[MMIDDLE] and not mouse_consumed and not picker.focus and tool == "brush":
        (mx, my) = mouse_pos
        (mxl, myl) = mouse_last # Last mouse position
        mx -= TOOL_W # Exclude the tool window area
        mxl -= TOOL_W # Exclude the tool window area
        if mx > 0: # If we are in the editor window area
            if mx >= pix_x and mx < (pix_x + edit_window.get_w() * pix_size) and my >= pix_y and my < (pix_y + edit_window.get_h() * pix_size):
                # Pixel position (px, py)
                px0 = int((mx - pix_x) / pix_size)
                py0 = int((my - pix_y) / pix_size)
                px1 = int((mxl - pix_x) / pix_size)
                py1 = int((myl - pix_y) / pix_size)
                if px0 >= 0 and px0 < edit_window.get_w() and py0 >= 0 and py0 < edit_window.get_h():
                    if px1 >= 0 and px1 < edit_window.get_w() and py1 >= 0 and py1 < edit_window.get_h():
                        _palette_index = selected_palette
                        if mouse_down[MRIGHT]:
                            _palette_index = selected_secondary  
                        for point in line(px0, py0, px1, py1):
                            edit_window.set_pixel(point, _palette_index)

    if mouse_clicked[MLEFT] or mouse_clicked[MRIGHT] and tool == "fill":
        (mx, my) = mouse_pos
        mx -= TOOL_W # Exclude the tool window area
        if mx > 0:
            if mx >= pix_x and mx < (pix_x + edit_window.get_w() * pix_size) and my >= pix_y and my < (pix_y + edit_window.get_h() * pix_size):
                px = int((mx - pix_x) / pix_size)
                py = int((my - pix_y) / pix_size)
        
                _palette_index = selected_palette
                if mouse_clicked[MRIGHT]:
                    _palette_index = selected_secondary

                replace_index = edit_window.get_pixel((px, py))
                            
                edit_window.set_pixel((px, py), _palette_index)

                _open = [(px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)]
                _visited = [(px, py)]
                            
                while len(_open) > 0:
                    _current = _open.pop(0)
                    if _current in _visited or edit_window.get_pixel(_current) != replace_index:
                        continue
                    _visited.append(_current)
                    edit_window.set_pixel(_current, _palette_index)
                    _open.append((_current[0] - 1, _current[1])) # Left
                    _open.append((_current[0] + 1, _current[1])) # Right
                    _open.append((_current[0], _current[1] - 1)) # Up
                    _open.append((_current[0], _current[1] + 1)) # Down
    
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
                picker.set_color(palette[selected_palette].color)

    palette[selected_palette].color = picker.get_color()

# Render

    screen.fill((0, 0, 0))
    edit_surface.fill((200, 200, 200))
    
    pyg.draw.rect(screen, (170, 170, 170), (0, 0, 125, SCREEN_H))

    edit_window.render(edit_surface, (pix_x, pix_y), pix_size, grid_button.is_down())

    screen.blit(edit_surface, (TOOL_W, 0))

    for (i, pc) in enumerate(palette):
        pc.render(screen, selected_palette, selected_secondary)
        edit_window.palette[i] = pc.color

    for button in buttons:
        button.render(assets, screen, font)

    picker.render(screen, font)
    
    pyg.display.flip()

    mouse_clicked = [False, False, False]
    mouse_released = [False, False, False]
    mouse_scroll = 0
    mouse_delta = [0, 0]
