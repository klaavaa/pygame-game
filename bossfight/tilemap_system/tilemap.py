import pygame
from spritesheet import SpriteSheet
TILEWIDTH, TILEHEIGHT = (64, 64)
class Tile(object):
    def __init__(self, x, y, file, collision, id):
        self.x = x
        self.y = y
        self.file = file
        self.collision = collision
        self.width = TILEWIDTH
        self.height = TILEHEIGHT
        self.rect = pygame.Rect(self.x * self.width, self.y * self.height, self.width, self.height)
        self.id = id

    def draw(self, win, cx, cy):
        self.file.draw(win, self.id - 1, self.x * self.width - cx, self.y * self.height - cy)




class Tilemap:
    def __init__(self, sprtsheet):
        self.tile_width = TILEWIDTH
        self.tile_height = TILEHEIGHT
        self.spritesheet = SpriteSheet(sprtsheet, 4, 4)
    def get_tile_1(self, x, y, id):
        return Tile(x, y, self.spritesheet, False, id)

    def get_tile_2(self, x, y, id):

        return Tile(x, y, self.spritesheet, True, id)

    def get_tile_3(self, x, y, id):
        return Tile(x, y, self.spritesheet, True, id)

    def get_tile_4(self, x, y, id):

        return Tile(x, y, self.spritesheet, True, id)

    def switcher(self, args, x, y):
        statements = {1: self.get_tile_1,
                      2: self.get_tile_2,
                      3: self.get_tile_3,
                      4: self.get_tile_4}



        func = statements.get(args, None)

        if func is not None:
            return func(x, y, args)

    def clean_up(self, arr):
        collisonobj = []
        while None in arr:
            arr.remove(None)

        for i, obj in sorted(enumerate(arr), reverse=True):
            if obj.collision:
                collisonobj.append((obj.x, obj.y))


        return arr, collisonobj

    def create_map(self, array):
        objects = []
        for y in range(len(array)):
            for x in range(len(array[y])):
                objects.append(self.switcher(array[y][x], x, y))

        return self.clean_up(objects)

    def create_array(self, object_list):
        array = []
        maxX, maxY = 0, 0
        minX, minY = 0, 0
        for object in object_list:
            maxX = max(maxX, object.x)
            maxY = max(maxY, object.y)
            minX = min(minX, object.x)
            minY = min(minY, object.y)


        maxX += 1 - minX + 2
        maxY += 1 - minY + 2

        for y in range(maxY):
            array.append([])
            for x in range(maxX):
                array[y].append(0)

        for object in object_list:
            array[object.y - minY + 1][object.x - minX + 1] = object.id

        return array

    def create_collision_array(self, coordinates):
        array = []
        maxX, maxY = 0, 0
        minX, minY = 0, 0
        for object in coordinates:
            maxX = max(maxX, object[0])
            maxY = max(maxY, object[1])
            minX = min(minX, object[0])
            minY = min(minY, object[1])


        maxX += 1 - minX + 2
        maxY += 1 - minY + 2

        for y in range(maxY):
            array.append([])
            for x in range(maxX):
                array[y].append(0)

        for object in coordinates:
            array[object[1] - minY + 1][object[0] - minX + 1] = 1

        return array

    def up(self, objects):
        for obj in objects:
            obj.x += 1
            obj.y += 1

        return objects
