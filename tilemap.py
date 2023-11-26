NEIGHTBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1) ,(1, 0) ,(0, 0) ,(-1, 1) ,(0, 1), (1, 1)]
#^^ this is looking for the distancein between the object from a tile around 9 others
#to handle collisions efficiently, you need to know how to look up tiles
#You want to know the nearby tiles near the player, around 9 tiles away, instead of all of them

PHYSICS_TILES = {"grass", "stone"} #set

import pygame
import json

class Tilemap:
    def __init__(self, game,tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # square grind of tiles
        self.offgrid_tiles = [] #things placed all over the place 

    def extract(self, id_pairs, keep = False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    def tiles_around(self, pos):
        tiles = [] #returning tiles
        tile_location = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) 
        #converts the pos, thats giving pixel position, into a grid position
        for offset in NEIGHTBOR_OFFSETS: #generates all the tiles arund the pixel position given
            check_location = str(tile_location[0] + offset[0]) + ";" + str(tile_location[1] + offset[1])
            if check_location in self.tilemap: #looks if there is an actual til e in there, no blank empty space
                tiles.append(self.tilemap[check_location])
        return tiles
    
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def solid_check(self, pos):
        tile_location = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_location in self.tilemap:
            if self.tilemap[tile_location]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_location]

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES: #this are the tiles we can collde with
                rects.append(pygame.Rect(tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size)) #it ask for tile_size twice since its a square
                 # asks for x and y axis in pixel position
        return rects

    def render(self, surface, offset=(0, 0)):
        for tile in self.offgrid_tiles: #the background details get render fisrt so it doesnt overlap incorrectley
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1])) #its applied negatively to move the camera acoordingly to the player, left to left, right to right
        
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = str(x) + ";" + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]))
        
        # for location in self.tile_map:
        #     tile = self.tile_map[location]
            #tile["type]": looks for the images with said name
            #tile["variant"]: is the index of said image
            #tile["pos"]: looks intot he position its in
            #it has to multiple by the tile size,