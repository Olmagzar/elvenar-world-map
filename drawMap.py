#!/usr/bin/python

import math
from PIL import Image, ImageDraw

h = 4096
w = 4096
L = 7

space = (20, 30, 40)
space = 'black'

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

    @property
    def col_width(self):
        return self.edge_length * 2

    @property
    def row_height(self):
        return math.sin(math.pi / 3) * self.edge_length

    def __call__(self, row, col):
        x = col * 3/2 * self.edge_length + h/2
        y = (2 * row + col) * self.row_height + w/2
        for angle in range(0, 360, 60):
            x += math.cos(math.radians(angle)) * self.edge_length
            y += math.sin(math.radians(angle)) * self.edge_length
            yield x
            yield y

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

def addCity(offset_x, offset_y, radius, draw, hexagon_generator, draw_aura = True):
    offset_y = offset_y - math.ceil(offset_x / 2)
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
                color = getColor(rad_aura)
                color = (color[0] + 10 * m_r,
                         color[1] + 10 * m_r,
                         color[2] + 10 * m_r)

                hexagon = hexagon_generator(row, col)
                draw.polygon(list(hexagon), color)

conf = [
        { "name": "JMT", "x": -113, "y": -68, "scout": 49459 },
        { "name": "Rose", "x": -73, "y": -44, "scout": 48830 },
        { "name": "Letraz", "x": 9, "y": -77, "scout": 54202 },
        { "name": "Micha", "x": 25, "y": 7, "scout": 47408 },
        { "name": "Laplus", "x": -97, "y": -65, "scout": 38550 },
        { "name": "Salvi", "x": -49, "y": 118, "scout": 44744 },
        { "name": "gradlon", "x": 78, "y": 72, "scout": 40112 },
        { "name": "Dura", "x": 135, "y": -80, "scout": 34031 },
        { "name": "As", "x": 155, "y": 34, "scout": 25489 },
        { "name": "Ares", "x": 79, "y": 19, "scout": 21797 },
        { "name": "wisch", "x": -92, "y": 36, "scout": 32223 },
        { "name": "ram", "x": -23, "y": -107, "scout": 21313 },
        { "name": "wizard", "x": 83, "y": 28, "scout": 26954 },
        { "name": "Fari", "x": 55, "y": -38, "scout": 21636 },
        { "name": "moar", "x": -112, "y": -30, "scout": 27294 },
        { "name": "Zeus", "x": 94, "y": 72, "scout": 15769 },
        { "name": "Julia", "x": 62, "y": -114, "scout": 18056 },
        { "name": "poupou", "x": -35, "y": -2, "scout": 6569 },
        { "name": "Cirederf", "x": -8, "y": 39, "scout": 6836 },
        { "name": "Jabal", "x": 111, "y": -89, "scout": 7328 },
        { "name": "Uruk", "x": -119, "y": 64, "scout": 5795 },
        { "name": "Zoubou", "x": 79, "y": -17, "scout": 64 }
        ]

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
    image = Image.new('RGB', (w, h), space)
    draw = ImageDraw.Draw(image)
    hexagon_generator = HexagonGenerator(L)
    max_row = math.ceil(h / L)
    max_col = math.ceil(w / (L * 3/2))
    for player in conf:
        player_r = getRadius(player["scout"])
        """print(player["name"], "radius:", player_r, ", category:", getCategory(player_r))"""
        addCity(player["x"], player["y"], getRadius(player["scout"]), draw, hexagon_generator)

    """draw.polygon(list(hexagon_generator(0, 0)), 'green')"""

    image.show()


main()
