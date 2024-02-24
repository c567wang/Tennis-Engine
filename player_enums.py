from enum import Enum, IntEnum

"""
# deprecated
class MovementState(Enum):
    SPLITSTEP = 0
    SLIDE = 1
    SPRINT = 2
"""

class DominantHand(Enum):
    LEFT = 1
    RIGHT = 2
    
class CourtHalf(IntEnum):
    # court perspective changing, so this is only where they start
    TOP = 0
    BOTTOM = 1