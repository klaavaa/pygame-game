import math, pygame
from timer import Timer
from useful_functions import *
class Fireball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.r = 5
        self.angle = angle
        self.speed = 1000
        self.damage = 10

        self.dx, self.dy = math.cos(self.angle), math.sin(self.angle)

    def update(self, dt):
        self.x = self.x + self.dx * (self.speed * dt)
        self.y = self.y + -self.dy * (self.speed * dt)

    def draw(self, win, cx, cy):
        pygame.draw.circle(win, (255, 0, 0), (int(self.x - cx), int(self.y - cy)), self.r)


class Pyroblast:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.r = 5
        self.angle = angle
        self.speed = 1000
        self.timer = Timer(5)
        self.damage = 100
        self.dx, self.dy = math.cos(self.angle), math.sin(self.angle)

    def calc_angle(self):
        self.dx, self.dy = math.cos(self.angle), math.sin(self.angle)

    def update(self, dt):
        self.x = self.x + self.dx * (self.speed * dt)
        self.y = self.y + -self.dy * (self.speed * dt)

    def draw(self, win, cx, cy):
        pygame.draw.circle(win, (255, 255, 0), (int(self.x - cx), int(self.y - cy)), self.r)

class CollisionCircle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self, win, cx, cy):
        pygame.draw.circle(win, (255, 0, 0), (int(self.x - cx), int(self.y - cy)), self.r)

sword = get_img('images/sword.png')

class SwordProjectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 400
        self.angle = angle
        self.damage = 20
        self.image = sword
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.img_copy = pygame.transform.rotate(self.image, self.angle * 180 / math.pi - 90)
        self.dx, self.dy = math.cos(self.angle), math.sin(self.angle)
        rect = self.img_copy.get_rect()
        center = rect.center
        x, y = self.x + center[0] + -self.dx, self.y + center[1] + self.dy
        x1, y1 = self.x + center[0] + -self.dx * -10, self.y + center[1] + self.dy * -10
        x2, y2 = self.x + center[0] + -self.dx * -20, self.y + center[1] + self.dy * -20
        x3, y3 = self.x + center[0] + -self.dx * -30, self.y + center[1] + self.dy * -30

        self.collision_circles = [CollisionCircle(x, y, 5), CollisionCircle(x1, y1, 5), CollisionCircle(x2, y2, 5), CollisionCircle(x3, y3, 5)]

    def update(self, dt):
        self.x += self.dx * (self.speed * dt)
        self.y += -self.dy * (self.speed * dt)
        for i in self.collision_circles:
            i.x += self.dx * (self.speed * dt)
            i.y += -self.dy * (self.speed * dt)

    def draw(self, win, cx, cy):
        win.blit(self.img_copy, (self.x - cx, self.y - cy))

      # for circle in self.collision_circles:
      #     circle.draw(win, cx, cy)


class Burn:
    def __init__(self, target):
        self.dps = 10
        self.target = target
        self.timer = Timer(10)

    def get_damage(self, dt):
        return self.dps * dt

    def update(self, dt):
        self.target.hp -= self.get_damage(dt)
        self.timer.update(dt)

        if self.timer.time <= 0:
            self.target.debuffs.remove(self)


poison = get_img('images/poison.png')
class PoisonBubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 64
        self.timer = Timer(5)
        self.target = None

        self.online_timer = Timer(2)
        self.online = False

        self.image = poison

    def update_online_timer(self, dt):
        self.online_timer.update(dt)
        if self.online_timer.time <= 0:
            self.online = True

    def hit(self, target):
        self.target = target
        self.target.stun()


    def update(self, dt):
        self.timer.update(dt)
        if self.timer.time <= 0:
            self.target.unstun()
            return True

        return False

    def draw(self, win, cx, cy):
        if not self.online:
            pygame.draw.circle(win, (255, 0, 0), (int(self.x - cx), int(self.y - cy)), self.r, 2)
        else:
            win.blit(self.image, (self.x - cx - self.r, self.y - cy - self.r))





