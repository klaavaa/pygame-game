from boss_system.character_pathfind import *
from animation_player import animationManager, animation
import pygame
from spritesheet import SpriteSheet
from timer import Timer
from skill import *
class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 64
        self.height = 64
        self.hw = self.width/2
        self.hh = self.height/2

        self.OriginalSpeed = 100
        self.speed = self.OriginalSpeed

        self.OriginalHP = 1000
        self.hp = self.OriginalHP

        self.pf = PathFind(self)
        self.am = animationManager.AnimationManager()

        self.state = States.IDLE
        self.idle_state = States.RIGHT
        self.freezetimer = Timer(10, done=True)
        self.freezetime = 10

        self.swordtime = 1.5
        self.swordcd = Timer(self.swordtime, done=True)

        self.timers = [self.freezetimer, self.swordcd]

        self.projectile_list = []

        self.load_sprites()


    def load_sprites(self):
        self.ch_ss = pygame.image.load('animations/player_sheet.png')
        self.ch_ss = pygame.transform.scale(self.ch_ss, (64 * 4, 64 * 4))
        self.ch_ss = SpriteSheet(self.ch_ss, 4, 4)

        self.r = animation.Animation('r', 400, 400, 20, self.ch_ss, 12, 15)
        self.l = animation.Animation('l', 400, 400, 20, self.ch_ss, 8, 11)
        self.u = animation.Animation('u', 400, 400, 20, self.ch_ss, 4, 7)
        self.d = animation.Animation('d', 400, 400, 20, self.ch_ss, 0, 3)

        self.idle = 0

        self.am.register_animation([self.r, self.l, self.u, self.d])


    def update(self, dt):
        self.am.update_pos([self.r, self.l, self.u, self.d], self.x, self.y)
        self.state = States.IDLE
        self.idle = self.idle_state.value * 4
        self.pf.update_move(dt)

        for projectile in self.projectile_list:
            projectile.update(dt)

        if self.state != States.IDLE:
            self.idle_state = self.state

        self.update_timers(dt)

    def match(self, win, cx, cy):
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

        self.match(win, cx, cy)
        self.am.update(win, cx, cy)

        # HITBOX
        pygame.draw.rect(win, (255, 0, 0), (self.x - cx, self.y - cy, self.width, self.height), 3)

        # HP BAR
        x, y = self.x - 10 - cx, self.y + self.height + 20 - cy
        pygame.draw.rect(win, (255, 0, 0), (x, y, 84, 10))
        if self.hp > 0:
            pygame.draw.rect(win, (0, 255, 0), (x, y, self.hp / self.OriginalHP * 84, 10))

        for projectile in self.projectile_list:
            projectile.draw(win, cx, cy)

    def freeze_effect(self):
        self.freezetimer.reset()
        self.speed *= 0.1

    def update_timers(self, dt):
        for timer in self.timers:
            timer.update(dt)
            if timer:
                timer.reset_and_pause()
                if timer == self.freezetimer:
                    self.speed = 100

    def cast_sword(self, angle):
        if self.swordcd.time == self.swordtime and self.swordcd.done:
            self.projectile_list.append(SwordProjectile(self.x, self.y, angle))
            self.swordcd.done = False
