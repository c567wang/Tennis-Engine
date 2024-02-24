from enum import Enum, IntEnum

class Hand(Enum):
    FOREHAND = 0
    BACKHAND = 1
    CENTERED = 2 # tweener or overheads (both forehand and backhand)
    
class Spin(IntEnum):
    FLAT = 0
    TOPSPIN = 1
    BACKSPIN = 2
    SIDESPIN_LEFT = 3
    SIDESPIN_RIGHT = 4
    
class Window(IntEnum):
    EV = 0 # early volley
    V = 1 # volley
    HV = 2 # half-volley
    GS = 3 # ground stroke
    # OHEV = 5 # overhead early volley
    # OHV = 6 # overhead volley
    # OHHV = 7 # overhead half-volley
    # OHGS = 8 # overhead ground stroke