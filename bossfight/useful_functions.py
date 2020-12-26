TW, TH = 64, 64
def get_tilemap_pos(x, y):
    return int(x / TW), int(y / TH)


def get_world_pos(x, y):
    return x * TH, y * TW
