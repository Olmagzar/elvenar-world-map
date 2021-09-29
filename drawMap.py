#!/usr/bin/python

import math
from PIL import Image, ImageDraw, ImageFont

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
                { "name": "As", "x": -91, "y": -35, "scout": 25489 },
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
                { "name": "Zoubou", "x": 157, "y": 67, "scout": 64 }
            ] },
        { "name": "deux couronnes", "members": [
                { "name":"tadou", "x": 20, "y": 75, "scout": 58194 },
                { "name":"Bluebell", "x": -105, "y": 55, "scout": 43578 },
                { "name":"Melusine", "x": 69, "y": -62, "scout": 41866 },
                { "name":"Ganghar", "x": -114, "y": 90, "scout": 33360 },
                { "name":"Florizette", "x": 74, "y": 33, "scout": 37516 },
                { "name":"Ka", "x": -6, "y": 147, "scout": 26828 },
                { "name":"Moqueur", "x": -130, "y": 30, "scout": 33930 },
                { "name":"miniphi", "x": 89, "y": -83, "scout": 28298 },
                { "name":"timotee", "x": 151, "y": -65, "scout": 35250 },
                { "name":"vince", "x": -139, "y": -71, "scout": 49160 },
                { "name":"daveHawai", "x": 123, "y": -89, "scout": 48151 },
                { "name":"Boree", "x": 94, "y": 75, "scout": 32236 },
                { "name":"maxiphi", "x": -73, "y": 79, "scout": 24558 },
                { "name":"Nibel", "x": 137, "y": -8, "scout": 20752 },
                { "name":"felindra", "x": -16, "y": 51, "scout": 19736 },
                { "name":"Abiwe", "x": 40, "y": -33, "scout": 20664 },
                { "name": "Jjidem", "x": 88, "y": -78, "scout": 18256 },
                { "name":"Seleme", "x": 46, "y": -114, "scout": 18288 },
                { "name":"Sylpheris", "x": -97, "y": 79, "scout": 13270 },
                { "name":"Wei Shilong", "x": -88, "y": -57, "scout": 8469 },
                { "name":"cbkhayman", "x": 75, "y": -80, "scout": 6903 },
                { "name":"lilour", "x": -78, "y": 72, "scout": 6288 },
                { "name":"ellebasi", "x": -6, "y": 150, "scout": 5160 },
                { "name":"Troll", "x": -11, "y": 148, "scout": 6468 },
            ] },
        #{ "name": "Odyssée", "members": [
        #        { "name": "Mexi", "x": -124, "y": 87, "scout": 30132 },
        #        { "name": "Famas", "x": 58, "y": -93, "scout": 19332 },
        #        { "name": "Castillo", "x": -109, "y": 58, "scout": 9792 },
        #        { "name": "Barnabiii", "x": -106, "y": 54, "scout": 9952 },
        #        { "name": "Dummy", "x": 76, "y": 81, "scout": 2496 },
        #        { "name": "Harry", "x": -60, "y": -33, "scout": 2394 },
        #        { "name": "Euterpe", "x": -2, "y": -81, "scout": 1896},
        #        { "name": "eloana", "x": -87, "y": 163, "scout": 900 }
        #    ] }
        ]

#conf = guildes[0]["members"]
h = 4096
w = 4096
L = 7

prefix_path = '/tmp/'

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
        image.save(prefix_path + guildes[0]["name"] + '_overlap.png')

    #draw.polygon(list(hexagon_generator(0, 0)), 'green')

main()
