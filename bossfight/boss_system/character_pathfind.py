from math import sqrt

from attr import asdict

from useful_functions import *
from states import States
from states import Action
from pathfinding_algs.astar import astar
from pathfinding_algs.bfs import bfs
class PathFind:
    def __init__(self, character):
        self.character = character
        self.index = 0
        self.past_index = self.index

        self.move_range = 2
        self.move_corners = False

        self.action = Action.MOVE

        self.dx, self.dy = 0, 0
        self.dmx, self.dmy = 0, 0

        self.path = None
        self.bfs_path = None
        self.drawable_path = None

        self.stop = False

    def in_range_bfs(self, x, y):
        for i in self.bfs_path:
            if i.x == x and i.y == y:
                return True

        return False

    def dist_between(self, x, y):
        return sqrt(pow(x - self.character.x * self.character.width, 2) + pow(y - self.character.y * self.character.height, 2))


    def delta_normalized(self, pos2):
        neg_x, neg_y = 0, 0
        x, y = get_world_pos(pos2.x, pos2.y)
        dx, dy = x - self.character.x, y - self.character.y

        if dx > 0:
            neg_x = 1
            self.character.state = States.RIGHT

        elif dx < 0:
            neg_x = -1
            self.character.state = States.LEFT

        if dy > 0:
            neg_y = 1
            self.character.state = States.DOWN

        elif dy < 0:
            neg_y = -1
            self.character.state = States.UP

        if dx != 0:
            dx = dx / dx * neg_x * self.character.speed
        else:
            dx = 0
        if dy != 0:
            dy = dy / dy * neg_y * self.character.speed
        else:
            dy = 0

        return dx, dy


    def move(self, next_node, dt):
        x, y = get_world_pos(next_node.x, next_node.y)
        if self.character.x - 5 < x < self.character.x + 5 and self.character.y - 5 < y < self.character.y + 5:
            self.character.x = x
            self.character.y = y
            self.character.am.remove_all()
            return True
        else:
            dv = self.delta_normalized(next_node)
            self.character.x += dv[0] * dt
            self.character.y += dv[1] * dt


    def pathfind(self, x, y, object_list):
        self.path = astar(get_tilemap_pos(self.character.x, self.character.y), (x, y), object_list)

        if self.path:
            self.path.reverse()

    def update(self, mx, my, obj_list):
        if self.dx != mx or self.dy != my:
            self.bfs_path = bfs(self.move_range, mx, my, self.move_corners, obj_list)


    def update_move(self, dt):

        if self.path:
            if self.index < len(self.path) - 1:
                if self.move(self.path[self.index + 1], dt):
                    self.index += 1
                if self.stop:
                    x, y = get_tilemap_pos(self.character.x, self.character.y)
                    x, y = get_world_pos(x, y)
                    if self.character.x - 5 < x < self.character.x + 5 and self.character.y - 5 < y < self.character.y + 5:
                        self.character.x = x
                        self.character.y = y
                        self.path = None
                        self.stop = False
                        self.index = 0
                        self.character.am.remove_all()

            else:
                self.path = None
                self.index = 0
