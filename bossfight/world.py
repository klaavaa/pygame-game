from tilemap_system.tilemap import Tilemap
import pygame
import os, sys
import pickle

class World:
    def load_level(self, n):
        with open(os.path.join(sys.path[0], f'level{n}.txt'), 'rb') as lvl:
            level = pickle.load(lvl)
        self.tm = Tilemap(pygame.image.load(os.path.join(sys.path[0], 'images', 'spritesheet.png')).convert())
        self.objects, self.collision_objects = self.tm.create_map(level)
        self.objects = self.tm.up(self.objects)
        self.collision_map = self.tm.create_collision_array(self.collision_objects)
