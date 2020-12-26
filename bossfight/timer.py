class Timer:
    def __init__(self, time, done=False):
        self.time = time
        self.ogtime = time
        self.done = done

    def update(self, dt):
        if not self.done:
            self.time -= dt

        if self.time < 0:
            self.time = 0
            self.done = True
    def __bool__(self):
        return self.time == 0

    def reset(self):
        self.time = self.ogtime
        self.done = False


    def reset_and_pause(self):
        self.time = self.ogtime
        self.done = True

    def continue_(self):
        self.done = False
