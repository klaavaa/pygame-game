from enum import Enum
class States(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
    IDLE = 4

class StageStates(Enum):
    MIDSTAGE = 0
    STAGE1 = 1
    STAGE2 = 2
    STAGE3 = 3
    STAGE4 = 4


class Action(Enum):
    MENU = 0
    MOVE = 1
    ATTACK = 2
    SKILL = 3