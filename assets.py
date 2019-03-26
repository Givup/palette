import pygame as pyg

class Assets:
    def __init__(self):
        self._images = {}
        self.reload()

    def get_image(self, name):
        if type(name) is list or type(name) is tuple:
            if len(name):
                return self._images[name[0]]
            return None
        return self._images[name]

    def reload(self):
        self._images.clear()
        self._images["color_wheel"] = pyg.image.load("icons/color_wheel.png")
        self._images["color_wheel_active"] = pyg.image.load("icons/color_wheel_active.png")
        self._images["grid"] = pyg.image.load("icons/grid.png")
        self._images["grid_active"] = pyg.image.load("icons/grid_active.png")
        self._images["logo"] = pyg.image.load("icons/logo.png")
