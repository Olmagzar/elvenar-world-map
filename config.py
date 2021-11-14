import math

fn = 'players.json'
h = 5500
w = 5500
L = 7

prefix_path = './maps/'

class ColorSet():
    def __init__(self, palette):
        if self.__class__ is ColorSet:
            raise Exception("Cannot instanciate from an abstract class")
        else:
            self.__background = (0, 0, 0)
            self.__axis = (92, 92, 92)
            self.__links = (128, 128, 128)
            self.__palette = palette

    def __getBackground(self):
        return self.__background
    def __getAxis(self):
        return self.__axis
    def __getLinks(self):
        return self.__links
    def __getPalette(self):
        return self.__palette

    background = property(__getBackground)
    axis = property(__getAxis)
    links = property(__getLinks)
    palette = property(__getPalette)

    def getColorIdx(self, value):
        pass

class StellarSet(ColorSet):
    def __init__(self):
        self.__stellar_color = [
            (0xff, 0x45, 0x00),
            (0xff, 0xae, 0x42),
            (0xef, 0xe4, 0x9a),
            (0xd8, 0xd7, 0xdf),
            (0x9a, 0xd7, 0xff),
            (0x4a, 0x8f, 0xdf),
            (0x0b, 0x50, 0xaf),
        ]
        super().__init__(self.__stellar_color)
    def getColorIdx(self, city_r):
        solar_r = 6
        solar_c = 2
        radius_per_c = (solar_r / solar_c)
        category = math.floor(city_r / radius_per_c)
        index = min(category, len(self.palette) - 1)
        return index

class OverlapSet(ColorSet):
    def __init__(self):
        self.__overlap_color = [
            (0, 127, 192),
            (192, 127, 0)
        ]
        super().__init__(self.__overlap_color)
    def getColorIdx(self, isForeignFS):
        if isForeignFS == True:
            index = 1
        else:
            index = 0
        return index

class ForestSet(ColorSet):
    def __init__(self):
        self.__forest_color = [
            (0x00, 0x99, 0x00),
            (0x99, 0xcc, 0x00),
            (0xcc, 0x99, 0x00),
            (0xcc, 0x33, 0x00),
            (0x66, 0x33, 0x00),
            (0x00, 0x00, 0x00),
        ]
        super().__init__(self.__forest_color)
    def getColorIdx(self, value):
        index = int((35 - value)/7)
        return index
