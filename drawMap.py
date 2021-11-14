#!/usr/bin/python

import os
import json
import math
from PIL import Image, ImageDraw, ImageFont
#from config import guildes

fn = 'active_players.json'
fd = os.open(fn, os.O_RDONLY)
sz = os.path.getsize(fn)
buf = os.read(fd, sz)
os.close(fd)

guildes = [ { 'name': 'active-players', 'members': json.loads(buf.decode()) } ]
h = 5500
w = 5500
L = 7

prefix_path = './maps/'

space = (0, 0, 0)
axis = (92, 92, 92) # Or (128, 128, 128)?
stellar_color = [
        (0xff, 0x45, 0x00),
        (0xff, 0xae, 0x42),
        (0xef, 0xe4, 0x9a),
        (0xd8, 0xd7, 0xdf),
        (0x9a, 0xd7, 0xff),
        (0x4a, 0x8f, 0xdf),
        (0x0b, 0x50, 0xaf),
        ]

stellar_set = [
        space,
        axis,
        (128, 128, 128),
        stellar_color
        ]

class Map():
    # TODO: Add colorset parameter
    def __init__(self, width, height, bg_color, axis_color, edge_length, title):
        self.__width = width
        self.__height = height
        self.__edge_length = edge_length
        self.bg_color = bg_color
        self.axis_color = axis_color
        self.title = title
        self.__image = Image.new('RGB', (self.__width, self.__height), self.bg_color)
        self.__draw = ImageDraw.Draw(self.__image)
        self.font = ImageFont.truetype('/usr/share/fonts/droid/DroidSans.ttf', 64)

    def putAxis(self):
        self.__draw.line((self.__edge_length,
                          self.__height/2,
                          self.__width - self.__edge_length,
                          self.__height/2),
                         self.axis_color, int(self.__edge_length/2))
        self.__draw.line((self.__width/2,
                          self.__edge_length,
                          self.__width/2,
                          self.__height - self.__edge_length),
                         self.axis_color, int(self.__edge_length/2))

    def save(self, prefix_path):
        if not os.path.isdir(prefix_path):
            try:
                os.mkdir(prefix_path)
            except:
                print('Unable to create directory', prefix_path)
                exit(1)
        self.__image.save(prefix_path + self.title)

    def clear(self):
        self.__draw((0, 0, self.__width, self.__height), self.bg_color)

    #  _|_._      \|
    #   |     ->   |\
    #   |          | \
    @staticmethod
    def __gametoHexCoord(row, col):
        hex_col = col
        hex_row = row - math.floor(col / 2)
        return (hex_row, hex_col)

    def __hexCoordToXYpx(self, hex_row, hex_col):
        hex_h = math.sin(math.pi / 3) * self.__edge_length
        ox = hex_col * 3/2 * self.__edge_length + self.__width/2
        oy = (2 * hex_row + hex_col) * hex_h + self.__height/2
        return (ox, oy)

    def __getCenterPx(self, city):
        (row, col) = self.__gametoHexCoord(row = city["y"], col = city["x"])
        return self.__hexCoordToXYpx(row, col)

    def __hexagon(self, row, col):
        (ox, oy) = self.__hexCoordToXYpx(row, col)
        for angle in range(0, 360, 60):
            x = math.cos(math.radians(angle)) * self.__edge_length + ox
            y = math.sin(math.radians(angle)) * self.__edge_length + oy
            yield x
            yield y

    def addCity(self, player, draw_aura = True, use_color = None):
        (offset_y, offset_x) = self.__gametoHexCoord(col = player["x"], row = player["y"])
        radius = getRadius(player["encounter"])
        rad_aura = radius
        if (not draw_aura):
            radius = 0
        radius += 1
        for row in range(-radius, radius):
            row += offset_y
            for col in range(-radius, radius):
                col += offset_x

                local_r = self.__tileDist(row_1 = offset_y, col_1 = offset_x,
                                          row_2 = row,      col_2 = col)
                if (local_r < radius):
                    m_r = radius - local_r
                    if not use_color:
                        # NOTE: should it always be dimmed?
                        color = getColor(rad_aura)
                        color = (color[0] + 10 * m_r,
                                 color[1] + 10 * m_r,
                                 color[2] + 10 * m_r)
                    else:
                        color = use_color

                    old_color = self.__draw.im.getpixel(self.__hexCoordToXYpx(row, col))
                    # NOTE: overlap part, should it be a specified argument?
#                    if old_color != space:
#                        color = (int((color[0] + old_color[0]) / 2),
#                                 int((color[1] + old_color[1]) / 2),
#                                 int((color[2] + old_color[2]) / 2))
#                        print(player["name"], "override color", old_color)

                    self.__draw.polygon(list(self.__hexagon(row, col)), color)

    # NOTE: Maybe should let these into a HexGameGeom(GameGeom) object.
    def __cityDist(self, city_1, city_2):
        (row_1, col_1) = self.__gametoHexCoord(col = city_1["x"], row = city_1["y"])
        (row_2, col_2) = self.__gametoHexCoord(col = city_2["x"], row = city_2["y"])
        return self.__tileDist(row_1, col_1, row_2, col_2)

    @staticmethod
    def __tileDist(row_1, col_1, row_2, col_2):
        return int((abs(col_2 - col_1) + abs(row_2 - row_1) + abs(col_2 + row_2 - col_1 - row_1)) / 2)

    def __prim(self, cities):
        sz = len(cities)
        distMatrix = []
        for city in cities:
            localDist = [ self.__cityDist(city, neighbour)
                          for neighbour in cities ]
            distMatrix.append(localDist)
        # Start of generic prim
        resultTree = []
        selectedVertices = [ False for i in range(sz) ]
        posInf = float('inf')
        while False in selectedVertices:
            minima = posInf
            start = end = 0
            for i in range(sz):
                if selectedVertices[i]:
                    for j in range(sz):
                        if (not selectedVertices[j] and distMatrix[i][j] > 0):
                            if distMatrix[i][j] < minima:
                                minima = distMatrix[i][j]
                                start, end = i, j
            selectedVertices[end] = True
            if minima != posInf:
                # TODO: check if this part cannot ignore the geometric details
                #       to export prim as a generic algorithm and wrap __prim
                #       around it to apply to class map
                p1 = self.__getCenterPx(cities[start])
                p2 = self.__getCenterPx(cities[end])
                resultTree.append(p1 + p2)
        # End of prim
        return resultTree

    def addLinks(self, cities):
        for line in self.__prim(cities):
            self.__draw.line(line, self.axis_color, int(self.__edge_length/2))

    # TODO: Add name function/option somewhere
    # TODO: Add legend -> implies color regulation instead of user choice

def getCategory(city_r):
    solar_r = 6
    solar_c = 2
    radius_per_c = (solar_r / solar_c)
    category = math.floor(city_r / radius_per_c)
    index = min(category, len(stellar_color) - 1)
    return index

def getColor(city_r):
    index = getCategory(city_r)
    return stellar_color[index]

# NOTE: should 'tiles' and getRadius be part of class map as they are
#       bound to game geometry details?
def tiles(n):
    entier = math.floor(n/3)
    extra = 0
    for k in range(3 * entier, n + 1):
        extra += (k * math.floor( (2*k + 1) / 3 ))
    return (3 * entier * ( (entier - 1) * (2 * entier + 1) + 1) + extra)

def getRadius(points):
    n = math.floor((points/48) ** (1/3))
    while (48 * tiles(n)) < points:
        n += 1
    return (n - 1)

def main():
    for conf in guildes:
        my_map = Map(w, h, space, axis, L, '{}.png'.format(conf['name']))
        my_map.putAxis()
        # Draw the current fellowship with aura of each members and save it
        print('Nb of active players: {}'.format(len(conf['members'])))
        for player in conf["members"]:
            # TODO: use class map
            my_map.addCity(player, draw_aura = False)
        my_map.save(prefix_path)
#    my_map.clear()
#
        # Draw the current fellowship without aura but add name of members
        # and minimal spanning tree using prim algorithm

#        for player in conf["members"]:
#            addCity(player, draw, draw_aura = False)
#        for player in conf["members"]:
#            (ox, oy) = getCenterPx(player)
#            txt_sz = draw.textsize(player["name"], font)
#            draw.text((ox - txt_sz[0]/2, oy - 5 * L - txt_sz[1]),
#                      player["name"],
#                      getColor(getRadius(player["encounter"])),
#                      font)
#
#    if len(guildes) < 2:
#        exit(0)
#    draw.line((L, h/2, w - L, h/2), (92, 92, 92), int(L/2))
#    draw.line((w/2, L, w/2, h - L), (92, 92, 92), int(L/2))
#    for conf in guildes:
#        # Draw overlap of all fellowship to see trading opportunities
#        if conf["name"] == guildes[0]["name"]:
#            use_color = (0, 127, 192)
#        else:
#            use_color = (192, 127, 0)
#        for player in conf["members"]:
#            addCity(player, draw, draw_aura = True, use_color = use_color)
main()
