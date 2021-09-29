#!/usr/bin/python

import math
from PIL import Image, ImageDraw, ImageFont

drawAura = True
guildes = [
        { "name": "pti Ros'Ours", "members": [
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
            ] },
        { "name": "Odyssée", "members": [
                { "name": "Mexi", "x": -124, "y": 87, "scout": 30132 },
                { "name": "Famas", "x": 58, "y": -93, "scout": 19332 },
                { "name": "Castillo", "x": -109, "y": 58, "scout": 9792 },
                { "name": "Barnabiii", "x": -106, "y": 54, "scout": 9952 },
                { "name": "Dummy", "x": 76, "y": 81, "scout": 2496 },
                { "name": "Harry", "x": -60, "y": -33, "scout": 2394 },
                { "name": "Euterpe", "x": -2, "y": -81, "scout": 1896},
                { "name": "eloana", "x": -87, "y": 163, "scout": 900 }
            ] }
        ]

#conf = guildes[0]["members"]
h = 4096
w = 4096
L = 7

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

def getCenter(x, y):
    (row, col) = toHexCoord(row = y, col = x)
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

def main():
    image = Image.new('RGB', (w, h), space)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/droid/DroidSans.ttf', 64)
    hexagon_generator = HexagonGenerator(L)
    for conf in guildes:
        # Draw the current fellowship with aura of each members and save it
        for player in conf["members"]:
            addCity(player, draw, hexagon_generator, draw_aura = True)
        image.save(conf["name"] + '_aura.png')

        # Clear
        draw.rectangle((0, 0, w, h), space)

        # Draw the current fellowship without aura but add name of members
        for player in conf["members"]:
            addCity(player, draw, hexagon_generator, draw_aura = False)
        for player in conf["members"]:
            (ox, oy) = getCenter(player["x"], player["y"])
            txt_sz = draw.textsize(player["name"], font)
            draw.text((ox - txt_sz[0]/2, oy - 5 * L - txt_sz[1]),
                      player["name"],
                      getColor(getRadius(player["scout"])),
                      font)
        image.save(conf["name"] + '_named.png')

        # Clear
        draw.rectangle((0, 0, w, h), space)

    for conf in guildes:
        # Draw overlap of all fellowship to see trading opportunities
        if conf["name"] == guildes[0]["name"]:
            use_color = (0, 127, 192)
        else:
            use_color = (192, 127, 0)
        for player in conf["members"]:
            addCity(player, draw, hexagon_generator, draw_aura = drawAura, use_color = use_color)
        image.save(guildes[0]["name"] + '_overlap.png')

    #draw.polygon(list(hexagon_generator(0, 0)), 'green')

main()
