import math

fn = 'players.json'
h = 5500
w = 5500
L = 7

prefix_path = './maps'

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
        self.__legend_title = 'City encounter radius'
        self.__legend = {
            (0xff, 0x45, 0x00): '< 3 tiles',
            (0xff, 0xae, 0x42): '< 6 tiles',
            (0xef, 0xe4, 0x9a): '< 9 tiles',
            (0xd8, 0xd7, 0xdf): '< 12 tiles',
            (0x9a, 0xd7, 0xff): '< 15 tiles',
            (0x4a, 0x8f, 0xdf): '< 18 tiles',
            (0x0b, 0x50, 0xaf): '> 18 tiles'
        }
        super().__init__([color for color in self.__legend])
    def __getLegend(self):
        return self.__legend
    def __getLegendTitle(self):
        return self.__legend_title

    legend = property(__getLegend)
    legend_title = property(__getLegendTitle)

    def getColorIdx(self, city_r):
        solar_r = 6
        solar_c = 2
        radius_per_c = (solar_r / solar_c)
        category = math.floor(city_r / radius_per_c)
        index = min(category, len(self.palette) - 1)
        return index

class OverlapSet(ColorSet):
    def __init__(self):
        self.__legend_title = 'Active players in the past 10 days'
        self.__legend = {
            (0x0b, 0x50, 0xaf): 'fellow members (all)',
            (0xff, 0x45, 0x00): 'foreign guild members',
            (0xef, 0xe4, 0x9a): 'players without guild'
        }
        super().__init__([color for color in self.__legend])
    def __getLegend(self):
        return self.__legend
    def __getLegendTitle(self):
        return self.__legend_title

    legend = property(__getLegend)
    legend_title = property(__getLegendTitle)

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
        self.__background = (0x03, 0x16, 0x24)
        self.__legend_title = 'Player last seen'
        self.__legend = {
            (0x00, 0x99, 0x00): '< 24h',
            (0x99, 0xcc, 0x00): '1 week ago',
            (0xcc, 0x99, 0x00): '2 weeks ago',
            (0xcc, 0x33, 0x00): '3 weeks ago',
            (0x46, 0x33, 0x00): '4 weeks ago or more'
        }
        self.__forest_color_i = [ color for color in self.__legend ]
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
        self.__forest_color.append(self.__forest_color_i[
            len(self.__forest_color_i) - 1])
        super().__init__(self.__forest_color)
    def __getBackground(self):
        return self.__background
    def __getLegend(self):
        return self.__legend
    def __getLegendTitle(self):
        return self.__legend_title

    background = property(__getBackground)
    legend = property(__getLegend)
    legend_title = property(__getLegendTitle)

    def getColorIdx(self, value):
        index = min((35 - value), len(self.palette) - 1)
        return index
