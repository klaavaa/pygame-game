from enum import Enum
class States(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
    IDLE = 4


class Action(Enum):
    MENU = 0
    MOVE = 1
    ATTACK = 2
    SKILL = 3