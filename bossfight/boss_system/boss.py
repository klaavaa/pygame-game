from boss_system.character_pathfind import *
from animation_player import animationManager, animation
import pygame
from spritesheet import SpriteSheet
from timer import Timer
from skill import *
from states import *

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

        self.poisontime = 7
        self.poisoncd = Timer(self.poisontime, done=True)

        self.castpoisontime = 1
        self.castpoison = Timer(self.castpoisontime, done=True)

        self.stage2time = 10
        self.stage2cd = Timer(self.stage2time, done=True)

        self.stage3time = 3
        self.stage3cd = Timer(self.stage3time, done=True)

        self.stage4time = 21
        self.stage4cd = Timer(self.stage4time, done=True)

        self.timers = [self.freezetimer, self.swordcd, self.poisoncd, self.castpoison]

        self.projectile_list = []
        self.debuffs = []

        self.finding_path = True

        self.stage = StageStates(1)

        self.angle = 0
        self.shot = True
        self.load_sprites()


    def load_sprites(self):
        self.ch_ss = pygame.image.load(os.path.join(sys.path[0], 'animations/player_sheet.png'))
        self.ch_ss = pygame.transform.scale(self.ch_ss, (64 * 4, 64 * 4))
        self.ch_ss = SpriteSheet(self.ch_ss, 4, 4)

        self.r = animation.Animation('r', 400, 400, 20, self.ch_ss, 12, 15)
        self.l = animation.Animation('l', 400, 400, 20, self.ch_ss, 8, 11)
        self.u = animation.Animation('u', 400, 400, 20, self.ch_ss, 4, 7)
        self.d = animation.Animation('d', 400, 400, 20, self.ch_ss, 0, 3)

        self.idle = 0

        self.fire = pygame.image.load(os.path.join(sys.path[0], 'images/fire.png'))
        self.am.register_animation([self.r, self.l, self.u, self.d])


    def update(self, dt):
        self.am.update_pos([self.r, self.l, self.u, self.d], self.x, self.y)
        self.state = States.IDLE
        self.idle = self.idle_state.value * 4
        self.pf.update_move(dt)

        for debuff in self.debuffs:
            debuff.update(dt)


        for projectile in self.projectile_list:
            if type(projectile) == SwordProjectile:
                projectile.update(dt)

        if self.state != States.IDLE:
            self.idle_state = self.state

        if self.stage == StageStates.STAGE1 and self.shot:
            if self.hp <= 0.5 * self.OriginalHP:
                self.stage = StageStates.MIDSTAGE



        if self.stage == StageStates.STAGE2:
            self.shot = False
            if self.stage2cd:
                self.stage = StageStates.STAGE3
            if self.stage2cd.done:
                self.stage2cd.done = False
            self.stage2cd.update(dt)

        if self.stage == StageStates.STAGE3:
            if self.stage3cd.done:
                self.stage3cd.done = False
            self.stage3cd.update(dt)
            if self.stage3cd:
                for i in self.projectile_list:
                    i.newangle(math.pi + i.angle)

                self.stage = StageStates.STAGE4

        if self.stage == StageStates.STAGE4:
            if self.stage4cd.done:
                self.stage4cd.done = False

            self.stage4cd.update(dt)
            if self.stage4cd:
                self.swordtime = 1
                self.swordcd.ogtime = self.swordtime
                self.swordcd.time = self.swordtime
                self.swordcd.done = True
                self.stage = StageStates.STAGE1

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

        for debuff in self.debuffs:
            if type(debuff) == Burn:
                win.blit(self.fire, (x + 86, y - 5))

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
            if self.stage == StageStates.STAGE2:
                self.projectile_list.append(SwordProjectile(self.x, self.y, math.pi + angle))
                self.angle += 0.2
            self.swordcd.done = False

    def deal_damage(self, skill, num=None):
        if self.stage == StageStates.STAGE1:
            if num is None:
                self.hp -= skill.damage
            else:
                self.hp -= num
        if self.hp < 0:
            self.hp = 0

    def cast_poison(self, cx, cy):
        if self.poisoncd.time == self.poisontime and self.poisoncd.done:
            self.projectile_list.append(PoisonBubble(cx, cy))
            self.poisoncd.done = False

    def attack(self, bossangle, cx, cy):
        if self.stage == StageStates.STAGE1:
            self.cast_sword(bossangle)
            self.cast_poison(cx, cy)
        else:
            if self.swordcd.ogtime != 0.1:
                self.swordcd.ogtime = 0.1
                self.swordcd.time = 0.1
                self.swordtime = 0.1
                self.swordcd.done = True
            if self.stage == StageStates.STAGE2:
                self.cast_sword(bossangle)
