#!/usr/bin/python

import os
import sys
import argparse
import json
import math
from PIL import Image, ImageDraw, ImageFont
import config

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

# Game geometry: hexagons
class GameGeom():
    def __init__(self, width, height, edge_length):
        self.__width = width
        self.__height = height
        self.__edge_length = edge_length

    #  _|_._      \|
    #   |     ->   |\
    #   |          | \
    @staticmethod
    def gameToGeomCoord(row, col):
        hex_col = col
        hex_row = row - math.floor(col / 2)
        return (hex_row, hex_col)

    def __geomCoordToXYpx(self, hex_row, hex_col):
        hex_h = math.sin(math.pi / 3) * self.__edge_length
        ox = hex_col * 3/2 * self.__edge_length + self.__width/2
        oy = (2 * hex_row + hex_col) * hex_h + self.__height/2
        return (ox, oy)

    def getCenterPx(self, city):
        (row, col) = self.gameToGeomCoord(row = city["y"], col = city["x"])
        return self.__geomCoordToXYpx(row, col)

    def tile(self, row, col):
        (ox, oy) = self.__geomCoordToXYpx(row, col)
        for angle in range(0, 360, 60):
            x = math.cos(math.radians(angle)) * self.__edge_length + ox
            y = math.sin(math.radians(angle)) * self.__edge_length + oy
            yield x
            yield y

    @staticmethod
    def tileDist(row_1, col_1, row_2, col_2):
        return int((abs(col_2 - col_1) + abs(row_2 - row_1) + abs(col_2 + row_2 - col_1 - row_1)) / 2)

    def cityDist(self, city_1, city_2):
        (row_1, col_1) = self.gameToGeomCoord(col = city_1["x"], row = city_1["y"])
        (row_2, col_2) = self.gameToGeomCoord(col = city_2["x"], row = city_2["y"])
        return self.tileDist(row_1, col_1, row_2, col_2)

    def range(self, center, radius):
        tile_set = []
        (offset_y, offset_x) = self.gameToGeomCoord(col = center["x"],
                                                    row = center["y"])
        for row in range(-radius, radius):
            row += offset_y
            for col in range(-radius, radius):
                col += offset_x
                local_r = self.tileDist(row_1 = offset_y, col_1 = offset_x,
                                        row_2 = row,      col_2 = col)
                if (local_r < radius):
                    tile_set.append({ 'm_r': (radius - local_r), 'coords': self.tile(row, col) })
        return tile_set

class Map():
    def __init__(self, width, height, edge_length, color_set, title):
        self.__width = width
        self.__height = height
        self.__edge_length = edge_length
        self.__geom = GameGeom(self.__width, self.__height, self.__edge_length)
        self.__color_set = color_set
        self.__title = title
        self.__image = Image.new('RGB', (self.__width, self.__height),
                                 self.__color_set.background)
        self.__draw = ImageDraw.Draw(self.__image)
        self.__font = ImageFont.truetype('/usr/share/fonts/droid/DroidSans.ttf', 64)

    def putAxis(self):
        self.__draw.line((self.__edge_length,
                          self.__height/2,
                          self.__width - self.__edge_length,
                          self.__height/2),
                         self.__color_set.axis, int(self.__edge_length/2))
        self.__draw.line((self.__width/2,
                          self.__edge_length,
                          self.__width/2,
                          self.__height - self.__edge_length),
                         self.__color_set.axis, int(self.__edge_length/2))

    def save(self, prefix_path):
        if not os.path.isdir(prefix_path):
            try:
                os.mkdir(prefix_path)
            except:
                print('Unable to create directory', prefix_path)
                exit(1)
        self.__image.save('{}{}.png'.format(prefix_path, self.__title))

    def clear(self):
        self.__draw((0, 0, self.__width, self.__height), self.__color_set.background)

    def addCity(self, player, draw_aura = True):
        if draw_aura == 'Low':
            radius = 1
        elif draw_aura == True:
            radius = getRadius(player["encounter"])
        else:
            radius = 0
        radius += 1

        for tile in self.__geom.range(player, radius):
            m_r = tile['m_r'] - 1
            color_idx = player['color_idx']
            color = self.__color_set.palette[color_idx]
            color = (color[0] + 10 * m_r,
                     color[1] + 10 * m_r,
                     color[2] + 10 * m_r)

            if color != self.__color_set.background:
                self.__draw.polygon(list(tile['coords']), color)

    def __prim(self, cities):
        sz = len(cities)
        distMatrix = []
        for city in cities:
            localDist = [ self.__geom.cityDist(city, neighbour)
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
                p1 = self.__geom.getCenterPx(cities[start])
                p2 = self.__geom.getCenterPx(cities[end])
                resultTree.append(p1 + p2)
        # End of prim
        return resultTree

    def addLinks(self, cities):
        for line in self.__prim(cities):
            self.__draw.line(line, self.__color_set.links, int(self.__edge_length/2))

    def addNames(self, cities):
        for city in cities:
            color_idx = city['color_idx']
            color = self.__color_set.palette[color_idx]
            (ox, oy) = self.__geom.getCenterPx(city)
            txt_sz = self.__draw.textsize(city['name'], self.__font)
            self.__draw.text((ox - txt_sz[0]/2, oy - 5 * self.__edge_length - txt_sz[1]),
                             city["name"], color, self.__font)

    # TODO: Add legend

def createGuildMaps(guild):
    color_set = config.StellarSet()

    # 1) Draw the current fellowship with aura of each members and save it
    guild_map = Map(config.w, config.h, config.L, color_set, guild['name'])
    guild_map.putAxis()
    for player in guild['members']:
        color_idx = color_set.getColorIdx(getRadius(player['encounter']))
        player['color_idx'] = color_idx
        guild_map.addCity(player, draw_aura = True)
    guild_map.save(config.prefix_path + 'fellowship-aura/')
    del guild_map

    # 2) Draw the current fellowship without aura but add name of members
    #    and minimal spanning tree using prim algorithm
    guild_map = Map(config.w, config.h, config.L, color_set, guild['name'])
    guild_map.addLinks(guild['members'])
    for player in guild['members']:
        color_idx = color_set.getColorIdx(getRadius(player['encounter']))
        player['color_idx'] = color_idx
        guild_map.addCity(player, draw_aura = 'Low')
    guild_map.addNames(guild['members'])
    guild_map.save(config.prefix_path + 'fellowship-named/')

def main(fn = config.fn, draw_all = True, draw_actives = True, draw_guilds = False,
         guild_name = None, player_guild = None):
    fd = os.open(fn, os.O_RDONLY)
    sz = os.path.getsize(fn)
    buf = os.read(fd, sz)
    os.close(fd)
    data = json.loads(buf.decode())
    del buf
    cities = [ data[k] for k in data ]
    name = os.path.splitext(os.path.basename(fn))[0]

    if draw_all == True:
        color_set = config.StellarSet()
        stellar_map = Map(config.w, config.h, config.L, color_set, 'all-' + name)
        stellar_map.putAxis()
        for player in cities:
            color_idx = color_set.getColorIdx(getRadius(player['encounter']))
            player['color_idx'] = color_idx
            stellar_map.addCity(player, draw_aura = False)
        stellar_map.save(config.prefix_path)

    if draw_actives == True:
        color_set = config.ForestSet()
        forest_map = Map(config.w, config.h, config.L, color_set, 'active-' + name)
        forest_map.putAxis()
        for player in cities:
            color_idx = color_set.getColorIdx(player['active_period'])
            player['color_idx'] = color_idx
            forest_map.addCity(player, draw_aura = False)
        forest_map.save(config.prefix_path)

    guilds = {}
    for p in cities:
        if 'guild_id' in p and p['guild_id'] not in guilds:
            guilds[p['guild_id']] = { 'name': p['guild_name'], 'members': [p]}
        elif 'guild_id' in p:
            guilds[p['guild_id']]['members'].append(p)

    if draw_guilds == True:
        for guild_id in guilds:
            guild = guilds[guild_id]
            createGuildMaps(guild)

    elif guild_name != None:
        guild = [ guilds[guild_id] for guild_id in guilds if guilds[guild_id]['name'] == guild_name ]
        if len(guild) > 0:
            if len(guild) > 1:
                print("Found {} guilds with the name '{}'!".format(len(guild), guild_name))
            guild = guild[0]
            createGuildMaps(guild)
        else:
            print("No guild named '{}' found.".format(guild_name))

    elif player_guild != None:
        guild_id = [ p['guild_id'] for p in cities if 'guild_id' in p and p['name'] == player_guild ]
        if len(guild_id) > 0:
            if len(guild_id) > 1:
                print("Player '{}' is in more than one guild!".format(player_guild))
            guild_id = guild_id[0]
            guild = guilds[guild_id]
            createGuildMaps(guild)
        else:
            print("Player '{}' is not in any guild.".format(player_guild))


        # 3) Draw overlap of all fellowship to see trading opportunities

#    if len(guildes) < 2:
#        exit(0)
#    my_map = Map(config.w, config.h, config.L, overlap_set, 'overlap.png')
#    my_map.putAxis()
#    for conf in guildes:
#        if conf["name"] == guildes[0]["name"]:
#            color_idx = 0
#        else:
#            color_idx = 1
#        for player in conf["members"]:
#            my_map.addCity(player, color_idx, draw_aura = True)
#    my_map.save(config.prefix_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Draw maps of players from json database.')
    parser.add_argument('--all', action=argparse.BooleanOptionalAction,
                        default=True, type=bool, help='Draw map of all players')
    parser.add_argument('--actives', action=argparse.BooleanOptionalAction,
                        default=True, type=bool, help='Draw map of activity')
    parser.add_argument('--guilds', action=argparse.BooleanOptionalAction,
                        default=False, type=bool, help='Draw maps of each guild')
    parser.add_argument('--guild-name', type=str, help='Draw maps of the specified guild')
    parser.add_argument('--player-guild', type=str, help='Draw maps of the guild of the specified player')
    parser.add_argument('filename', type=str, help='json file containing all players')

    args = parser.parse_args(sys.argv[1:])
    draw_all = vars(args)['all']
    draw_actives = vars(args)['actives']
    draw_guilds = vars(args)['guilds']
    guild_name = vars(args)['guild_name']
    player_guild = vars(args)['player_guild']
    fn = vars(args)['filename']

    if not draw_all and not draw_actives and not draw_guilds and guild_name == None and player_guild == None:
        print("Nothing to do")
        print("Type '{} --help' to list options".format(sys.argv[0]))
        exit(0)
    if os.path.exists(fn) and os.path.isfile(fn):
        main(fn, draw_all, draw_actives, draw_guilds, guild_name, player_guild)
    else:
        print("File '{}' does not exist.".format(fn))
