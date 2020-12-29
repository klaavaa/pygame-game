
from vector2d import Vector2D
import math





drawlines = True
drawcircles = False
drawshapes = True


maxdist = 250
raycount = 10


class Point:
    def __init__(self, pos):
        self.pos = pos
        self.dir = 0

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

def lenght(v):
    return math.sqrt(pow(v.x, 2) + pow(v.y, 2))


def dsttobox(p, centre, size):
    offset = abs(p - centre) - size

    dx = max(offset.x, 0)
    dy = max(offset.y, 0)

    return lenght(Vector2D(dx, dy))

def dsttoboxfrombox(rect1, rect2):
    min_dist = float('-inf')

    c1 = Point(Vector2D(rect1.x + rect1.w / 2, rect1.y + rect1.h / 2))
    c2 = Point(Vector2D(rect2.x + rect2.w / 2, rect2.y + rect2.h / 2))

    dx = abs(c2.pos.x - c1.pos.x)
    dy = abs(c2.pos.y - c1.pos.y)

    if dx < (rect1.w + rect2.w) / 2 and dy >= (rect1.h + rect2.h) / 2:
        min_dist = dy - (rect1.h + rect2.h) / 2

    elif dx >= (rect1.w + rect2.w) / 2 and dy < (rect1.h + rect2.h) / 2:
        min_dist = dx - (rect1.w + rect2.w) / 2

    elif dx >= (rect1.w + rect2.w) / 2 and dy >= (rect1.h + rect2.h) / 2:
        delta_x = dx - (rect1.w + rect2.w) / 2
        delta_y = dy - (rect1.h + rect2.h) / 2
        min_dist = math.sqrt(delta_x * delta_x + delta_y * delta_y)

    else:
        min_dist = -1

    return min_dist

def dsttoscene(p, collision_tiles):
    dst = float('inf')

    for i in collision_tiles:
        x, y = i
        x, y = x * 64, y * 64
        w, h = 64, 64
        dsttob = dsttoboxfrombox(Rect(p.x, p.y, 32, 32), Rect(x, y, w, h))
        dst = min(dst, dsttob)

    return dst
