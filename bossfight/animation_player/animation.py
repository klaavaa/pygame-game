class Animation:
    def __init__(self, name, x, y, frame_per_img, spritesheet, i1=0, i2=None):
        self.x = x
        self.y = y
        self.name = name
        self.spritesheet = spritesheet
        self.frame_per_img = frame_per_img
        self.counter = 0
        self.index = i1
        self.first_index = i1

        self.last_index = spritesheet.cell_count - 1

        if i2 is not None:
            self.last_index = i2


    def draw(self, win, cx, cy):
        self.spritesheet.draw(win, self.index, self.x - cx, self.y - cy)


    def advance(self):
        self.counter += 1
        self.index = int(self.counter / self.frame_per_img) + self.first_index
        if self.index > self.last_index:
            self.counter = 0
            self.index = self.first_index
            return False
        return True

    def play(self, win, cx, cy):
        self.draw(win, cx, cy)
        return self.advance()

