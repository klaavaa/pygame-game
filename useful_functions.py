import sys, os
import random
import pygame
TW, TH = 64, 64
def get_tilemap_pos(x, y):
    return int(x / TW), int(y / TH)


def get_world_pos(x, y):
    return x * TH, y * TW


def rng(prosentti):

    return True if random.randint(0, 100) <= prosentti else False

def get_img(str):
    return pygame.image.load(os.path.join(sys.path[0], str))