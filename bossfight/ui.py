import pygame

class Icon:
    def __init__(self, x, y, width, height, image, globaltimer, timer=None, charge=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.timer = timer
        self.globaltimer = globaltimer
        self.surface = image
        self.charge = charge

        self.surface2 = pygame.Surface((self.width, self.height))
        self.surface2.fill((0, 0, 0))
        self.surface2.set_alpha(200)

        self.globalcdsurface = pygame.Surface((64, 64))
        self.globalcdsurface.fill((0, 0, 0))
        self.globalcdsurface.set_alpha(200)

    def draw(self, win, font):
        win.blit(self.surface, (self.x, self.y))

        if self.globaltimer is not None:
            temp = int((self.globaltimer.time / self.globaltimer.ogtime) * self.height)
            self.globalcdsurface = pygame.transform.scale(self.globalcdsurface, (self.width, temp))
            globaly = self.y + (self.height - temp)
        self.globalcdsurface.fill((0, 0, 0))
        self.surface2.fill((0, 0, 0))


        if self.charge is not None:
            text = font.render(f'{self.charge.n}', True, (255, 255, 255))
            win.blit(text, (self.x, self.y))
            if self.globaltimer is not None:
                if not self.globaltimer.done and self.globaltimer.time != self.globaltimer.ogtime:
                    win.blit(self.globalcdsurface, (self.x, globaly))
            if self.charge.n == 0:

                if self.timer is not None:
                    if not self.timer.done and self.timer.time != self.timer.ogtime:

                        win.blit(self.surface2, (self.x, self.y))
                        text = font.render(f'{int(self.timer.time)}', True, (255, 255, 255))
                        win.blit(text, (self.x + 20, self.y + 20))

        else:
            if self.globaltimer is not None:
                if not self.globaltimer.done and self.globaltimer.time != self.globaltimer.ogtime:
                    win.blit(self.globalcdsurface, (self.x, globaly))

            if self.timer is not None:
                if not self.timer.done and self.timer.time != self.timer.ogtime:
                    win.blit(self.surface2, (self.x, self.y))
                    text = font.render(f'{int(self.timer.time)}', True, (255, 255, 255))
                    win.blit(text, (self.x + 20, self.y + 20))


class UI:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 20)
        self.abilities = []

    def draw(self, win):
        for ability in self.abilities:
            ability.draw(win, self.font)

    def set_icon(self, x, y, width, height, image, globaltimer, timer, charge):
        self.abilities.append(Icon(x, y, width, height, image, globaltimer, timer, charge))




class Button:
    def __init__(self, x, y, width, height, image, image2, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.image2 = image2
        self.colliding = False
        self.id = id


    def check_collsion(self, mx, my):
        if self.x < mx < self.x + self.width and self.y < my < self.y + self.height:
            return True

        return False

    def update(self, mx, my):
        self.colliding = False
        if self.check_collsion(mx, my):
            self.colliding = True


    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        if self.colliding:
            win.blit(self.image2, (self.x, self.y))


