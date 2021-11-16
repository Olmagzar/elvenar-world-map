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
            (0x0b, 0x50, 0xaf),
            (0xff, 0x45, 0x00),
            (0xef, 0xe4, 0x9a)
        ]
        super().__init__(self.__overlap_color)
        self.__overlap_color.append(super().background)
    def getColorIdx(self, guild_id, player):
        if not 'guild_id' in player:
            index = 2
        elif player['guild_id'] == guild_id:
            index = 0
        else:
            index = 1
        return index

class ForestSet(ColorSet):
    def __init__(self):
        self.__background = (0x12, 0x0a, 0x00)
        self.__forest_color_i = [
            (0x00, 0x99, 0x00),
            (0x99, 0xcc, 0x00),
            (0xcc, 0x99, 0x00),
            (0xcc, 0x33, 0x00),
            self.__background
        ]
        self.__forest_color = []
        for i in range(len(self.__forest_color_i) - 1):
            col_1 = self.__forest_color_i[i]
            col_2 = self.__forest_color_i[i + 1]
            col_stp = ((col_2[0] - col_1[0])/7,
                       (col_2[1] - col_1[1])/7,
                       (col_2[2] - col_1[2])/7)
            for j in range(7):
                self.__forest_color.append((round(col_1[0] + j*col_stp[0]),
                                            round(col_1[1] + j*col_stp[1]),
                                            round(col_1[2] + j*col_stp[2])))
        self.__forest_color.append(self.__background)
        super().__init__(self.__forest_color)

    def __getBackground(self):
        return self.__background

    background = property(__getBackground)

    def getColorIdx(self, value):
        index = min((35 - value), len(self.palette) - 1)
        return index
