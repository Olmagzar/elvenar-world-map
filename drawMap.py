#!/usr/bin/python

import math
from PIL import Image, ImageDraw

"""h = 1900
w = 1900
L = 5
"""
h = 500
w = 500
L = 10
rx = 2
ry = 2

radius = 6 + 1

ville = (0, 0, 0)
space = (20, 30, 40)
marbre = (250, 235, 215)
planches = (205, 127, 50)
acier = (111, 127, 128)
cristal = (0, 255, 255)
parcho = (233, 214, 107)
soie = (237, 135, 45)
elixir = (224, 60, 49)
poussiere = (255, 166, 201)
gemmes = (189, 51, 164)
cl = 1/2

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

def getColor(city_r):
    solar_r = 6
    solar_c = 2
    radius_per_c = (solar_r / solar_c)
    stellar_color = [
            (0xff, 0x45, 0x00),
            (0xff, 0xae, 0x42),
            (0xef, 0xe4, 0x9a),
            (0xd8, 0xd7, 0xdf),
            (0x7a, 0xb7, 0xef),
            (0x5a, 0x9f, 0xef),
            (0x2b, 0x70, 0xcf),
            ]
    category = math.floor(city_r / radius_per_c)
    index = min(category, len(stellar_color) - 1)
    return stellar_color[index]

offset_x = 0
offset_y = 0

def main():
    image = Image.new('RGB', (w, h), space)
    draw = ImageDraw.Draw(image)
    hexagon_generator = HexagonGenerator(L)
    max_row = math.ceil(h / L)
    max_col = math.ceil(w / (L * 3/2))
    for row in range(-round(max_row/2), round(max_row/2)):
        for col in range(-round(max_col/2), round(max_col/2)):

            local_r = int((abs(col - offset_x) + abs(row - offset_y) + abs(col + row - offset_x - offset_y)) / 2) 
            if (local_r < radius):
                m_r = radius - local_r
                color = getColor(radius - 1)
                color = (color[0] + 10 * m_r,
                         color[1] + 10 * m_r,
                         color[2] + 10 * m_r)

                hexagon = hexagon_generator(row, col)
                draw.polygon(list(hexagon), color)
            """
            if (abs(col - offset_x) < radius and abs(col - offset_x + row - offset_y) < radius and abs(row - offset_y) < radius):
            elif ( abs(row - col) % 3 == 0 ):
                color = ville
            else:
                color = space

            elif ( col % 3 == 0 and (((row - 4) % 9) % 4) == 0):
                color = marbre
            elif ( col % 3 == 0 and (((row - 1) % 9) % 4) == 0):
                color = planches
            elif ( col % 3 == 0 and (((row + 2) % 9) % 4) == 0):
                color = acier

            elif ( (col - 1)% 3 == 0 and (((row + 4) % 9) % 4) == 0):
                color = cristal
            elif ( (col - 1) % 3 == 0 and (((row + 1) % 9) % 4) == 0):
                color = parcho
            elif ( (col - 1)% 3 == 0 and (((row - 2) % 9) % 4) == 0):
                color = soie

            elif ( (col - 2) % 3 == 0 and (((row + 3) % 9) % 4) == 0):
                color = elixir
            elif ( (col - 2)% 3 == 0 and (((row) % 9) % 4) == 0):
                color = poussiere
            elif ( (col - 2)% 3 == 0 and (((row - 3) % 9) % 4) == 0):
                color = gemmes
            """


    """
    hexagon = hexagon_generator(0, 0)
    draw.polygon(list(hexagon), 'green')
    hexagon = hexagon_generator(0, 1)
    draw.polygon(list(hexagon), 'green')
    hexagon = hexagon_generator(0, 2)
    draw.polygon(list(hexagon), 'blue')

    hexagon = hexagon_generator(1, 0)
    draw.polygon(list(hexagon), 'yellow')
    """
    image.show()


main()
