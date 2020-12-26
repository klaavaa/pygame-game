import math, pygame
from timer import Timer
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

class SwordProjectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 400
        self.angle = angle
        self.image = pygame.image.load('images/sword.png')
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



