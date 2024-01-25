from enum import Enum, IntEnum

class MovementState(Enum):
    SPLITSTEP = 0
    SLIDE = 1
    SPRINT = 2
    
class DominantHand(Enum):
    LEFT = 1
    RIGHT = 2
    
class CourtHalf(IntEnum):
    TOP = 0
    BOTTOM = 1