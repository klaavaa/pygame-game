class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.playing_animations = []

    def register_animation(self, animation):
        if type(animation) == list:
            for i in animation:
                self.animations[i.name] = i
        else:
            self.animations[animation.name] = animation

    def update(self, win, cx, cy):
        for i, animation in sorted(enumerate(self.playing_animations), reverse=True):
            if not animation.play(win, cx, cy):
                self.playing_animations.pop(i)

    def update_pos(self, name, newX, newY):
        if type(name) == list:
            for i in name:
                self.animations[i.name].x = newX
                self.animations[i.name].y = newY
        else:
            self.animations[name].x = newX
            self.animations[name].y = newY

    def get_pos(self, name):
        return self.animations[name].x, self.animations[name].y

    def play_animaton(self, name):
        self.playing_animations.append(self.animations[name])


    def is_playing(self, name):
        if self.animations[name] in self.playing_animations:
            return True

        return False


    def remove_all(self):
        self.playing_animations.clear()


    def remove(self, object):
        self.playing_animations.remove(object)

    def update_player_animation(self, name):
        if not self.is_playing(name):
            self.remove_all()
            self.play_animaton(name)






