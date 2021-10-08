#!/usr/bin/python

import os
import math
from PIL import Image, ImageDraw, ImageFont
from config import guildes

#conf = guildes[0]["members"]
h = 4096
w = 4096
L = 7

prefix_path = './maps/'

space = (0, 0, 0)
stellar_color = [
        (0xff, 0x45, 0x00),
        (0xff, 0xae, 0x42),
        (0xef, 0xe4, 0x9a),
        (0xd8, 0xd7, 0xdf),
        (0x9a, 0xd7, 0xff),
        (0x4a, 0x8f, 0xdf),
        (0x0b, 0x50, 0xaf),
        ]

class HexagonGenerator(object):
    """Returns a hexagon generator for hexagons of the specified size."""
    def __init__(self, edge_length):
        self.edge_length = edge_length

    def __call__(self, row, col):
        (ox, oy) = getXY(row, col, self.edge_length)
        for angle in range(0, 360, 60):
            x = math.cos(math.radians(angle)) * self.edge_length + ox
            y = math.sin(math.radians(angle)) * self.edge_length + oy
            yield x
            yield y

def getXY(hex_row, hex_col, hex_L):
    hex_h = math.sin(math.pi / 3) * hex_L
    ox = hex_col * 3/2 * hex_L + w/2
    oy = (2 * hex_row + hex_col) * hex_h + h/2
    return (ox, oy)

def toHexCoord(row, col):
    hex_col = col
    hex_row = row - math.ceil(col / 2)
    return (hex_row, hex_col)

def getCenter(player):
    (row, col) = toHexCoord(row = player["y"], col = player["x"])
    return getXY(row, col, L)

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

def addCity(player, draw, hexagon_generator, draw_aura = True, use_color = None):
    (offset_y, offset_x) = toHexCoord(col = player["x"], row = player["y"])
    radius = getRadius(player["scout"])
    rad_aura = radius
    if (not draw_aura):
        radius = 1
    radius += 1
    for row in range(-radius, radius):
        row += offset_y
        for col in range(-radius, radius):
            col += offset_x

            local_r = int((abs(col - offset_x) + abs(row - offset_y) + abs(col + row - offset_x - offset_y)) / 2)
            if (local_r < radius):
                m_r = radius - local_r
                if not use_color:
                    color = getColor(rad_aura)
                    color = (color[0] + 10 * m_r,
                             color[1] + 10 * m_r,
                             color[2] + 10 * m_r)
                else:
                    color = use_color

                hexagon = hexagon_generator(row, col)
                old_color = draw.im.getpixel(getXY(row, col, L))
                if old_color != space:
                    color = (int((color[0] + old_color[0]) / 2),
                             int((color[1] + old_color[1]) / 2),
                             int((color[2] + old_color[2]) / 2))
#                    print(player["name"], "override color", old_color)

                draw.polygon(list(hexagon), color)

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

def dist(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)

def tileDist(player_1, player_2):
    (row_1, col_1) = toHexCoord(col = player_1["x"], row = player_1["y"])
    (row_2, col_2) = toHexCoord(col = player_2["x"], row = player_2["y"])
    return int((abs(col_2 - col_1) + abs(row_2 - row_1) + abs(col_2 + row_2 - col_1 - row_1)) / 2)

def main():
    image = Image.new('RGB', (w, h), space)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/droid/DroidSans.ttf', 64)
    hexagon_generator = HexagonGenerator(L)

    if not os.path.isdir(prefix_path):
        try:
            os.mkdir(prefix_path)
        except:
            print('Unable to create directory', prefix_path)
            exit(1)

    for conf in guildes:
        # Draw the current fellowship with aura of each members and save it
        draw.line((L, h/2, w - L, h/2), (92, 92, 92), int(L/2))
        draw.line((w/2, L, w/2, h - L), (92, 92, 92), int(L/2))
        for player in conf["members"]:
            addCity(player, draw, hexagon_generator, draw_aura = True)
        image.save(prefix_path + conf["name"] + '_aura.png')

        # Clear
        draw.rectangle((0, 0, w, h), space)

        # Draw the current fellowship without aura but add name of members
        # and minimal spanning tree using prim algorithm
        confSize = len(conf["members"])
        distMatrix = []
        resultTree = []
        for player in conf["members"]:
#            localDist = [ dist(getCenter(player), getCenter(neighbour))
            localDist = [ tileDist(player, neighbour)
                          for neighbour in conf["members"] ]
            distMatrix.append(localDist)
        selectedVertices = [ False for i in range(confSize) ]
        posInf = float('inf')
        while False in selectedVertices:
            minima = posInf
            start = end = 0
            for i in range(confSize):
                if selectedVertices[i]:
                    for j in range(confSize):
                        if (not selectedVertices[j] and distMatrix[i][j] > 0):
                            if distMatrix[i][j] < minima:
                                minima = distMatrix[i][j]
                                start, end = i, j

            selectedVertices[end] = True
            if minima != posInf:
                p1 = getCenter(conf["members"][start])
                p2 = getCenter(conf["members"][end])
                resultTree.append(p1 + p2)

        for line in resultTree:
            draw.line(line, (128, 128, 128), int(L/2))


        for player in conf["members"]:
            addCity(player, draw, hexagon_generator, draw_aura = False)
        for player in conf["members"]:
            (ox, oy) = getCenter(player)
            txt_sz = draw.textsize(player["name"], font)
            draw.text((ox - txt_sz[0]/2, oy - 5 * L - txt_sz[1]),
                      player["name"],
                      getColor(getRadius(player["scout"])),
                      font)
        image.save(prefix_path + conf["name"] + '_named.png')

        # Clear
        draw.rectangle((0, 0, w, h), space)

    draw.line((L, h/2, w - L, h/2), (92, 92, 92), int(L/2))
    draw.line((w/2, L, w/2, h - L), (92, 92, 92), int(L/2))
    for conf in guildes:
        # Draw overlap of all fellowship to see trading opportunities
        if conf["name"] == guildes[0]["name"]:
            use_color = (0, 127, 192)
        else:
            use_color = (192, 127, 0)
        for player in conf["members"]:
            addCity(player, draw, hexagon_generator, draw_aura = True, use_color = use_color)
        image.save(prefix_path + guildes[0]["name"] + '_overlap_' + guildes[1]["name"] + '.png')

    #draw.polygon(list(hexagon_generator(0, 0)), 'green')

main()
