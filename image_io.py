import os

import png

from edit_window import *

import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog

working_directory = os.path.dirname(os.path.realpath(__file__))

def load():
    _filename = filedialog.askopenfilename(initialdir = working_directory, title = "Load PPA file", filetypes = (("PPA File", "*.ppa"), ("All files", "*.*")))
    if len(_filename) <= 0:
        return None
    _file = open(_filename, "r")
    
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


def save():
    _filename = filedialog.asksaveasfilename(initialdir = working_directory, title = "Save as", filetypes = (("PPA Files", "*.ppa"), ("All files", "*.*")))
    if len(_filename) <= 0:
        return
    file = open(_filename, "w")
    file.write("PPA1\n")
    file.write(str(edit_window.get_w()) + " " + str(edit_window.get_h()) + "\n")
    file.write(str(len(edit_window.palette)) + "\n")
    for p in range(len(edit_window.palette)):
        file.write(str(edit_window.palette[p][0]) + " " + str(edit_window.palette[p][1]) + " " + str(edit_window.palette[p][2]) + "\n")
    for pix in edit_window.pixels:
        file.write(str(pix) + " ")

def export_png():
    _filename = filedialog.asksaveasfilename(initialdir = working_directory, title = "Export file", filetypes = (("PNG File", "*.png"), ("All files", "*.*")))
    if len(_filename) <= 0:
        return
    file = open(_filename, "wb")
    w = png.Writer(size = edit_window.get_size(), greyscale = False, palette = edit_window.get_palette())
    w.write(file, edit_window.get_index_data())
    # w.write(f, edit_window.get_pixel_data())
    file.close()
    
def import_png():
    _filename = filedialog.askopenfilename(initialdir = working_directory, title = "Select import file", filetypes = (("PNG files", "*.png"), ("All files", "*.*")))
    #_filename = simpledialog.askstring("Import", "Filename", initialvalue="import.png")
    if _filename == None:
        return None
    if not _filename.endswith(".png"):
        _filename += ".png"
    try:
        _reader = png.Reader(filename = _filename)

        (_w, _h, _values, _info) = _reader.read_flat()

        _image = ImageEditWindow(_info["size"]);

        _is_palette = len(_info["palette"]) > 0

        if _is_palette:
            _image.palette = _info["palette"]
            _image.pixels = _values;
            return _image
        else:
            print("Non-palette images not supported currently.")
            return None
    except (TypeError, FileNotFoundError):
        print("Couldn't import", _filename)
        return None
