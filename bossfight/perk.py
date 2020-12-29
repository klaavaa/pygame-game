class CastingPerk:
    def __init__(self):
        self.percentage = 0.25

    def get_value(self, n):
        return (1 - self.percentage) * n