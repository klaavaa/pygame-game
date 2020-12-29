import pygame
from character import *
from timer import *
from skill import *
import pickle
from states import *
from useful_functions import get_tilemap_pos, get_world_pos, TW, TH, rng
import math
from tilemap_system.tilemap import *
import os
import sys
import math
from boss_system.boss import Boss
from ui import *
import random
from world import World
from networking.network import Network

pygame.init()
SW, SH = 800, 800
win = pygame.display.set_mode((SW, SH))

clock = pygame.time.Clock()
fps = 144

cam = Camera(64, 64)

world = World()
world.load_level(1)
ui = UI()

screen_rect = pygame.Rect(-100, -100, 1100, 1100)

def check_collision(c, x, y, w, h):

    cx = abs(c.x - (x + w / 2))
    cy = abs(c.y - (y + h / 2))

    if cx > (w / 2 + c.r):
        return False
    if cy > (h / 2 + c.r):
        return False

    if cx <= w / 2:
        return True
    if cy <= h / 2:
        return True
    cornerDistance_sq = (cx - w / 2) ** 2 + (cy - h / 2) ** 2

    return cornerDistance_sq <= c.r ^ 2

def circle_collision_rect(c):
    mx, my = get_tilemap_pos(c.x, c.y)
    if mx - 1 >= 0 and mx + 2 <= len(world.collision_map[0]) and my - 1 >= 0 and my + 2 <= len(world.collision_map):
        for i in range(my - 1, my + 2):
            for j in range(mx - 1, mx + 2):
                if world.collision_map[i][j] == 1:
                    x, y = get_world_pos(j, i)
                    if check_collision(c, x, y, TW, TH):
                        return True
    return False

def draw(c, c2=None, boss=None):

    win.fill(0)

    for obj in world.objects:
        if screen_rect.contains(pygame.Rect(obj.x * TW - cam.x, TH + obj.y * TH - cam.y, obj.width, obj.height)):
            obj.draw(win, cam.x, cam.y)


    c.draw(win, cam.x, cam.y)
    if c2:
        c2.draw(win, cam.x, cam.y)
    if boss:
        boss.draw(win, cam.x, cam.y)

    ui.draw(win)

    pygame.display.flip()

def tilemap_collision(collision_map, o):
    mx, my = get_tilemap_pos(o.x, o.y)
    if mx - 1 >= 0 and mx + 2 <= len(world.collision_map[0]) and my - 1 >= 0 and my + 2 <= len(world.collision_map):
        for i in range(my - 1, my + 2):
            for j in range(mx - 1, mx + 2):
                if world.collision_map[i][j] == 1:
                    x, y = get_world_pos(j, i)
                    ox = o.x < x + TW and o.x + o.width > x
                    oy = o.y < y + TH and o.y + o.height > y
                    if ox and oy:
                        return True
    return False

def rect_collision_detection(x1, y1, w1, h1, x2, y2, w2, h2):
    ox = x1 < x2 + w2 and x1 + w1 > x2
    oy = y1 < y2 + h2 and y1 + h1 > y2
    if ox and oy:
        return True
    return False

def update_boss(dt, c, boss):
    global globalcdsurface, globaly
    if c.hp > 0 and boss.hp > 0:
        keys = pygame.key.get_pressed()
        dx, dy = c.x, c.y
        mx, my = pygame.mouse.get_pos()
        angle = -math.atan2(my - (c.y + c.height/2 - cam.y), mx - (c.x + c.width/2 - cam.x))
        c.angle = angle
        c.state = States.IDLE
        c.am.remove_all()
        c.update(dt)


        mx, my = get_tilemap_pos(mx + cam.x, my + cam.y)
        cx, cy = get_tilemap_pos(c.x, c.y)
        bx, by = get_tilemap_pos(boss.x, boss.y)
        pygame.display.set_caption(f'mouse: ({mx, my}), player: ({cx, cy}), boss: ({bx, by}')

        boss.update(dt)

        if keys[pygame.K_SPACE]:
            c.cast(Fireball(c.x + c.width / 2, c.y + c.height / 2, c.angle))

        for index, projectile in sorted(enumerate(c.projectiles), reverse=True):
           #if projectile.x <= 0 + cam.x or projectile.x >= SW + cam.x or projectile.y >= SH + cam.y or projectile.y <= 0 + cam.y:
           #    c.projectiles.pop(index)
           #    continue

            if circle_collision_rect(projectile):
                c.projectiles.pop(index)
                continue

            if check_collision(projectile, boss.x, boss.y, boss.width, boss.height):
                c.projectiles.pop(index)
                if type(projectile) == Pyroblast:
                    for debuff in boss.debuffs:
                        if type(debuff) == Burn:
                            projectile.damage *= 2

                boss.deal_damage(projectile)
                if rng(10):
                    boss.debuffs.append(Burn(boss))



        for index, projectile in sorted(enumerate(boss.projectile_list), reverse=True):
           #if projectile.x <= 0 + cam.x or projectile.x >= SW + cam.x or projectile.y >= SH + cam.y or projectile.y <= 0 + cam.y:
           #    boss.projectile_list.pop(index)
           #    continue
            if projectile.x < -200 or projectile.x > 2000 or projectile.y < -200 or projectile.y > 2000:
                boss.projectile_list.pop(index)
                continue

            if type(projectile) == SwordProjectile:
                for circle in projectile.collision_circles:
                   #if circle_collision_rect(circle):
                   #    boss.projectile_list.pop(index)
                   #    break
                    if check_collision(circle, c.x, c.y, c.width, c.height):

                        boss.projectile_list.pop(index)
                        c.deal_damage(projectile)
                        break

            elif type(projectile) == PoisonBubble:
                if not projectile.online:
                    projectile.update_online_timer(dt)
                else:
                    if check_collision(projectile, c.x, c.y, c.width, c.height):
                        projectile.hit(c)

                    if projectile.target is not None:
                        if projectile.update(dt):
                            boss.projectile_list.pop(index)


        if keys[pygame.K_w]:
            c.y -= c.speed * dt
            c.state = States.UP
            c.casting = None

        if keys[pygame.K_s]:
            c.y += c.speed * dt
            c.state = States.DOWN
            c.casting = None

        collision = tilemap_collision(world.collision_map, c)
        if collision:
            c.y = dy

        if keys[pygame.K_d]:
            c.x += c.speed * dt
            c.state = States.RIGHT
            c.casting = None

        if keys[pygame.K_a]:
            c.x -= c.speed * dt
            c.state = States.LEFT
            c.casting = None
        collision = tilemap_collision(world.collision_map, c)
        if collision:
            c.x = dx

        if get_tilemap_pos(dx, dy) != get_tilemap_pos(c.x, c.y):
            boss.pf.stop = True

        if boss.pf.path is None:
            boss.pf.pathfind(cx, cy, world.collision_map)


        deltaX, deltaY = abs(boss.x + (boss.width / 2) - c.x + (c.width / 2)), abs(boss.y + (boss.height / 2) - c.y + (c.height / 2))
        deltaPos = math.sqrt(deltaX**2 + deltaY**2)
        multiplier = deltaPos / (400 * dt)

        x, y = c.x + (c.x - dx) * multiplier, c.y + (c.y - dy) * multiplier

        # BOSS SWORD CAST #


        if rng(20):
            bossangle = -math.atan2((y + c.height / 2)  - (boss.y + boss.height / 2), (x + c.width / 2) - (boss.x + boss.width / 2))
        else:
            bossangle = -math.atan2((c.y + c.height / 2) - (boss.y + boss.height / 2), (c.x + c.width / 2) - (boss.x + boss.width / 2))

        boss.attack(bossangle, c.x, c.y)

        if c.casting:
            c.casting.x = c.x + c.width / 2
            c.casting.y = c.y + c.height / 2
            c.casting.angle = angle
            c.casting.calc_angle()

        cam.update(c, SW, SH)

    else:
        print(f'Character hp: {c.hp}, boss hp: {boss.hp}')



def update_arena(dt, c, c2, dealt_skills):
    global globalcdsurface, globaly
    keys = pygame.key.get_pressed()
    dx, dy = c.x, c.y
    mx, my = pygame.mouse.get_pos()
    angle = -math.atan2(my - (c.y + c.height/2 - cam.y), mx - (c.x + c.width/2 - cam.x))
    c.angle = angle
    c.state = States.IDLE
    c.am.remove_all()
    c.update(dt)



    #mx, my = get_tilemap_pos(mx + cam.x, my + cam.y)
    cx, cy = get_tilemap_pos(c.x, c.y)
   #bx, by = get_tilemap_pos(boss.x, boss.y)
  # pygame.display.set_caption(f'mouse: ({mx, my}), player: ({cx, cy}), boss: ({bx, by}')


    if keys[pygame.K_SPACE]:
        c.cast(Fireball(c.x + c.width / 2, c.y + c.height / 2, c.angle))

    for index, projectile in sorted(enumerate(c.projectiles), reverse=True):

        if circle_collision_rect(projectile):
            c.projectiles.pop(index)
            continue

        if check_collision(projectile, c2.x, c2.y, c2.width, c2.height):
            c.projectiles.pop(index)
            #c2.deal_damage(projectile)
            dealt_skills.append(projectile)



#    print(c.hp)
    if keys[pygame.K_w]:
        c.y -= c.speed * dt
        c.state = States.UP
        if c.casting:
            c.casting = None
            c.pyrocd.reset_and_pause()

    if keys[pygame.K_s]:
        c.y += c.speed * dt
        c.state = States.DOWN
        if c.casting:
            c.casting = None
            c.pyrocd.reset_and_pause()

    collision = tilemap_collision(world.collision_map, c)
    if collision:
        c.y = dy

    if keys[pygame.K_d]:
        c.x += c.speed * dt
        c.state = States.RIGHT
        if c.casting:
            c.casting = None
            c.pyrocd.reset_and_pause()

    if keys[pygame.K_a]:
        c.x -= c.speed * dt
        c.state = States.LEFT
        if c.casting:
            c.casting = None
            c.pyrocd.reset_and_pause()

    collision = tilemap_collision(world.collision_map, c)
    if collision:
        c.x = dx

    if c.casting:
        c.casting.x = c.x + c.width / 2
        c.casting.y = c.y + c.height / 2
        c.casting.angle = angle
        c.casting.calc_angle()

    cam.update(c, SW, SH)


def boss_fight_game():
    run = True
    get_ticks_last_frame = pygame.time.get_ticks()
    c = Character(DummyCharacter(256, 256, 100, 100, 0, 100, [], 100, False))
    c.load_sprites()

    boss = Boss(1024, 1024)

    ui.set_icon(300, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/frostfirebolt.png')).convert(), c.skillcd, None, None)
    ui.set_icon(380, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/blink.png')).convert(), c.skillcd, c.blinkcd, c.blinkcharge)
    ui.set_icon(460, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/frost_nova.png')).convert(), c.skillcd, c.freezecd, None)
    ui.set_icon(540, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/pyroblast.png')).convert(), None, c.pyrocd, None)
    ui.set_icon(620, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/fire_shield.png')).convert(), c.skillcd, c.firecd, None)


    while run:

        mposX, mposY = pygame.mouse.get_pos()
        mposX, mposY = get_tilemap_pos(mposX + cam.x, mposY + cam.y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    c.cast(Fireball(c.x + c.width / 2, c.y + c.height / 2, c.angle))
                    c.casting = None

                if event.key == pygame.K_r:
                    c.blink(world.collision_objects)

                if event.key == pygame.K_3:
                    c.freeze(world.collision_map, boss)
                    c.casting = None

                if event.key == pygame.K_4:
                    c.cast_cd(Pyroblast(c.x + c.width / 2, c.y + c.height / 2, c.angle))

                if event.key == pygame.K_q:
                    c.fire_shield()

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #    if event.button == 1:
            #        boss.pf.pathfind(mposX, mposY, collision_map)
            #   if event.button == 3:
            #       boss.pf.stop = True
        clock.tick(fps)
        t = pygame.time.get_ticks()
        dt = (t - get_ticks_last_frame) / 1000
        get_ticks_last_frame = t
        pygame.display.set_caption(f'{int(1 / dt)}, {dt}ms delay')

        update_boss(dt, c, boss)
        draw(c, boss=boss)



def arena_game():

    run = True
    get_ticks_last_frame = pygame.time.get_ticks()
    n = Network()
    characters = n.get_c()
    c, c2 = Character(characters[0]), Character(characters[1])
    c.load_sprites()
    c2.load_sprites()

    ui.set_icon(300, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/frostfirebolt.png')).convert(), c.skillcd, None, None)
    ui.set_icon(380, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/blink.png')).convert(), c.skillcd, c.blinkcd, c.blinkcharge)
    ui.set_icon(460, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/frost_nova.png')).convert(), c.skillcd, c.freezecd, None)
    ui.set_icon(540, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/pyroblast.png')).convert(), None, c.pyrocd, None)
    ui.set_icon(620, 720, 64, 64, pygame.image.load(os.path.join(sys.path[0], 'images/fire_shield.png')).convert(), c.skillcd, c.firecd, None)

    while not n.request():
        font = pygame.font.SysFont('arial', 30)
        text = font.render('Waiting for another player', 1, (255, 255, 255))
        win.blit(text, (350, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        n.send(True)

    n.send(True)



    while run:

        dealt_skills = []

        dummy, c.hp, c.absorb_shield, c.speed = n.request()
       # c.deal_damage(dmg)

        n.send(c.get_dummy())
        c2.update_from_dummy(dummy)

        mposX, mposY = pygame.mouse.get_pos()
        mposX, mposY = get_tilemap_pos(mposX + cam.x, mposY + cam.y)

        das = c.absorb_shield



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    c.cast(Fireball(c.x + c.width / 2, c.y + c.height / 2, c.angle))
                    if c.casting:
                        c.casting = None
                        c.pyrocd.reset_and_pause()

                if event.key == pygame.K_r:
                    c.blink(world.collision_objects)

                if event.key == pygame.K_3:
                    c.freeze(world.collision_map, c2)
                    if c.casting:
                        c.casting = None
                        c.pyrocd.reset_and_pause()

                if event.key == pygame.K_4:
                    c.cast_cd(Pyroblast(c.x + c.width / 2, c.y + c.height / 2, c.angle))

                if event.key == pygame.K_q:
                    c.fire_shield()

        clock.tick(fps)
        t = pygame.time.get_ticks()
        dt = (t - get_ticks_last_frame) / 1000
        get_ticks_last_frame = t
        pygame.display.set_caption(f'{int(1/dt)}, {dt}ms delay')

        update_arena(dt, c, c2, dealt_skills)
        draw(c, c2)


        n.send([dealt_skills, c2.speed, c.absorb_shield - das])


def main():

    buttons = [Button(200, 600, 400, 200, pygame.image.load(os.path.join(sys.path[0], 'images/buttons/multiplayer_button.png')).convert()
                      , pygame.image.load(os.path.join(sys.path[0], 'images/buttons/multiplayer_button_highlited.png')).convert(), "multiplayer"),
               Button(200, 300, 400, 200, pygame.image.load(os.path.join(sys.path[0],'images/buttons/boss_fight_button.png')).convert(),
                      pygame.image.load(os.path.join(sys.path[0], 'images/buttons/boss_fight_button_highlited.png')).convert(), "bossfight")]
    run = True
    while run:
        win.fill(0)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if button.check_collsion(mx, my):
                            if button.id == "bossfight":
                                boss_fight_game()
                            elif button.id == "multiplayer":
                                arena_game()
                            run = False


        for button in buttons:
            button.update(mx, my)
            button.draw(win)

        pygame.display.update()
if __name__ == '__main__':
    main()

pygame.quit()
sys.exit()