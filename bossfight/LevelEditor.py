import pygame
import pickle
from tilemap_system.tilemap import Tilemap
import os
from spritesheet import SpriteSheet
import math

pygame.init()
win = pygame.display.set_mode((800, 600))
run = True

tm = Tilemap(pygame.image.load(os.path.join('images', 'spritesheet.png')))
slide = True

x, y = 0, 0
tile_size = 64
id = 1
object_list = []
def draw():
    win.fill(0)
    for object in object_list:
        object.draw(win, x, y)

    pygame.draw.rect(win, (200, 10, 0), (mx * tile_size - x, my * tile_size - y, tile_size, tile_size), 5)

    pygame.display.update()

def update():
    if slide:
        remove = False
        if pygame.mouse.get_pressed()[2]:
            remove = True
        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            tile = tm.switcher(id, mx, my)
            canappend = True
            for obj in object_list:
                if tile.x == obj.x and tile.y == obj.y:
                    canappend = False
                    tile2 = obj

            if canappend and not remove:
                object_list.append(tile)
            if remove and not canappend:
                object_list.remove(tile2)
    pygame.display.set_caption(f'x: {mx}, y: {my}')
while run:
    mx, my = pygame.mouse.get_pos()
    mx = math.floor((mx + x)/ tile_size)
    my = math.floor((my + y) / tile_size)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x -= 64

            if event.key == pygame.K_d:
                x += 64

            if event.key == pygame.K_w:
                y -= 64

            if event.key == pygame.K_s:
                y += 64
            if event.key == pygame.K_1:
                id = 1
            if event.key == pygame.K_2:
                id = 2
            if event.key == pygame.K_3:
                id = 3
            if event.key == pygame.K_4:
                id = 4
            if event.key == pygame.K_5:
                id = 5
            if event.key == pygame.K_6:
                id = 6
            if event.key == pygame.K_7:
                id = 7
            if event.key == pygame.K_8:
                id = 8
            if event.key == pygame.K_9:
                id = 9

            if event.key == pygame.K_RETURN:
                with open(f'level{id}.txt', "wb") as file:
                    pickle.dump(tm.create_array(object_list), file)
                    file.close()

            if event.key == pygame.K_BACKSPACE:
                try:
                    with open(f'level{id}.txt', 'rb') as file:

                        level = pickle.load(file)
                        file.close()
                    object_list, collision_list, enemies = tm.create_map(level)
                    object_list.extend(enemies)
                except:
                    print("no such level saved")
        if not slide:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    tile = tm.switcher(id, mx, my)
                    canappend = True
                    for obj in object_list:
                        if tile.x == obj.x and tile.y == obj.y:
                            canappend = False

                    if canappend:
                        object_list.append(tile)

    update()
    draw()


