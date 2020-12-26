import pygame
from animation_player import animation, animationManager
from spritesheet import *
from enum import Enum
import math
from useful_functions import get_tilemap_pos, get_world_pos
from pathfinding_algs.bfs import bfs
from timer import Timer
from states import *

class charge:
    def __init__(self, n):
        self.n = n

class DummyCharacter:
    def __init__(self, x, y, OriginalHP, hp, absorb_shield, speed, projectiles, state):
        self.x = x
        self.y = y
        self.OriginalHP = OriginalHP
        self.hp = hp
        self.absorb_shield = absorb_shield
        self.speed = speed
        self.projectiles = projectiles
        self.state = state

class Character:
    def __init__(self, dummy):
        self.x = dummy.x
        self.y = dummy.y
        self.width = 32
        self.height = 32

        self.OriginalHP = dummy.OriginalHP
        self.hp = dummy.hp
        self.absorb_shield = dummy.absorb_shield
        self.speed = dummy.speed
        self.projectiles = dummy.projectiles

        self.am = animationManager.AnimationManager()
        self.state = States.IDLE


        self.blinkrange = 200
        self.freezerange = 1

        self.angle = None



        self.time = 0.8
        self.blinktime = 18
        self.freezetime = 60
        self.pyrotime = 5
        self.shieldtime = 0.1

        self.blinkcharge = charge(2)

        self.skillcd = Timer(self.time, done=True)
        self.blinkcd = Timer(self.blinktime, done=True)
        self.freezecd = Timer(self.freezetime, done=True)
        self.pyrocd = Timer(self.pyrotime, done=True)
        self.firecd = Timer(self.shieldtime, done=True)

        self.freezetimer = Timer(10, done=True)
        self.freezedtime = 10

        self.timers = [self.skillcd, self.blinkcd, self.freezecd, self.pyrocd, self.freezetimer, self.firecd]
        self.casting = None

    def update_from_dummy(self, dummy):
        self.x = dummy.x
        self.y = dummy.y
        self.OriginalHP = dummy.OriginalHP
        self.hp = dummy.hp
        self.absorb_shield = dummy.absorb_shield
        self.speed = dummy.speed
        self.projectiles = dummy.projectiles
        self.state = dummy.state

    def get_dummy(self):
        return DummyCharacter(self.x, self.y, self.OriginalHP, self.hp, self.absorb_shield, self.speed, self.projectiles, self.state)

    def load_sprites(self):
        self.ch_ss = pygame.image.load('animations/player_sheet.png')
        self.ch_ss = pygame.transform.scale(self.ch_ss, (32 * 4, 32 * 4))
        self.ch_ss = SpriteSheet(self.ch_ss, 4, 4)

        self.r = animation.Animation('r', 400, 400, 20, self.ch_ss, 12, 15)
        self.l = animation.Animation('l', 400, 400, 20, self.ch_ss, 8, 11)
        self.u = animation.Animation('u', 400, 400, 20, self.ch_ss, 4, 7)
        self.d = animation.Animation('d', 400, 400, 20, self.ch_ss, 0, 3)
        self.idle = 0

        self.am.register_animation([self.r, self.l, self.u, self.d])


    def match(self, win, cx, cy):
        self.am.remove_all()
        if self.state == States.IDLE:
            self.ch_ss.draw(win, self.idle, self.x - cx, self.y - cy)

        elif self.state == States.LEFT:
            self.am.update_player_animation('l')

        elif self.state == States.RIGHT:
            self.am.update_player_animation('r')

        elif self.state == States.UP:
            self.am.update_player_animation('u')

        elif self.state == States.DOWN:
            self.am.update_player_animation('d')


    def draw(self, win, cx, cy):
        self.am.update_pos([self.r, self.l, self.u, self.d], self.x, self.y)
        self.match(win, cx, cy)
        self.am.update(win, cx, cy)

        #HITBOX
        pygame.draw.rect(win, (255, 0, 0), (self.x - cx, self.y - cy, self.width, self.height), 1)

        for projectile in self.projectiles:
            projectile.draw(win, cx, cy)

        # HP BAR
        x, y = self.x - 10 - cx, self.y + self.height + 20 - cy
        pygame.draw.rect(win, (255, 0, 0), (x, y, 52, 10))
        if self.hp > 0:
            pygame.draw.rect(win, (0, 255, 0), (x, y, self.hp / self.OriginalHP * 52, 10))

        if self.absorb_shield > 0:
            pygame.draw.rect(win, (153, 205, 209), (x + self.hp / self.OriginalHP * 52, y, self.absorb_shield / self.OriginalHP * 52, 10))

        if self.casting:
            castx = self.casting.timer.time / self.casting.timer.ogtime * 120
            pygame.draw.rect(win, (200, 40, 0), (self.x - cx - 44, self.y - cy + 75, 120, 15))
            pygame.draw.rect(win, (40, 100, 230), (self.x - cx - 44, self.y - cy + 75, castx, 15))

    def update_timers(self, dt):
        for timer in self.timers:
            timer.update(dt)
            if timer:
                if timer == self.blinkcd and self.blinkcharge.n < 2:
                    self.blinkcharge.n += 1
                    if self.blinkcharge.n < 2:
                        timer.reset()
                    else:
                        timer.reset_and_pause()
                else:
                    timer.reset_and_pause()

                if timer == self.freezetimer:
                    self.speed = 100


    def update(self, dt):

        for projectile in self.projectiles:
            projectile.update(dt)

        self.update_timers(dt)
        if self.casting is not None:
            self.casting.timer.update(dt)
            if self.casting.timer:
                self.projectiles.append(self.casting)
                self.casting = None
    def cast(self, Skill):
        if self.skillcd.time == self.time and self.skillcd.done:
            self.projectiles.append(Skill)
            self.skillcd.done = False

    def cast_cd(self, Skill):

        if self.pyrocd.time == self.pyrotime and self.pyrocd.done:
            self.casting = Skill
            self.pyrocd.done = False

    def blink(self):
        if self.skillcd.time == self.time and self.skillcd.done and( (self.blinkcd.time == self.blinktime and self.blinkcd.done) or 0 < self.blinkcharge.n < 2):
            self.x = self.x + math.cos(self.angle) * self.blinkrange
            self.y = self.y + -math.sin(self.angle) * self.blinkrange
            self.blinkcharge.n -= 1

            self.skillcd.done = False
            self.blinkcd.done = False


    def freeze(self, object_list, boss):
        if self.skillcd.time == self.time and self.skillcd.done and self.freezecd.time == self.freezetime and self.freezecd.done:
            x, y = get_tilemap_pos(self.x, self.y)
            path = bfs(self.freezerange, x, y, True, object_list)
            bx, by = get_tilemap_pos(boss.x, boss.y)
            for node in path:
                if node.x == bx and node.y == by:
                    boss.freeze_effect()

            self.skillcd.done = False
            self.freezecd.done = False

    def freeze_effect(self):
        self.freezetimer.reset()
        self.speed *= 0.1

    def fire_shield(self):
        if self.skillcd.time == self.time and self.skillcd.done and self.firecd.time == self.shieldtime and self.firecd.done:
            self.absorb_shield += self.OriginalHP * 0.25
            self.skillcd.done = False
            self.firecd.done = False

    def deal_damage(self, skill):
        if self.absorb_shield > 0:
            self.absorb_shield -= skill.damage
            if self.absorb_shield < 0:
                self.absorb_shield = 0
        else:
            self.hp -= skill.damage
            if self.hp < 0:
                self.hp = 0

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, character, screen_width, screen_height):
        self.x += (character.x - self.x - screen_width / 2 + character.width / 2) / 10
        self.y += (character.y - self.y - screen_height / 2 + character.height / 2) / 10




