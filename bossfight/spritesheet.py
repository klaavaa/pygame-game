class SpriteSheet:
    def __init__(self, spritesheet, cols, rows):
        self.spritesheet = spritesheet
        self.rows = rows
        self.cols = cols
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        w = self.cellW = self.rect.width / cols
        h = self.cellH = self.rect.height / rows
        self.cells = list([(index % cols * w, index // cols * h, w, h) for index in range(self.cell_count)])

    def draw(self, win, index, x, y):
        win.blit(self.spritesheet, (x, y), self.cells[index])

