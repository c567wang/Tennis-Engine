from enum import Enum, IntEnum

class Hand(Enum):
    FOREHAND = 1
    BACKHAND = 2
    CENTERED = 3 # tweener or overheads (both forehand and backhand)
    
class Spin(Enum):
    FLAT = 1
    TOPSPIN = 2
    BACKSPIN = 3
    SIDESPIN = 4
    
class Window(IntEnum):
    EV = 0 # early volley
    V = 1 # volley
    HV = 2 # half-volley
    GS = 3 # ground stroke
    # OHEV = 5 # overhead early volley
    # OHV = 6 # overhead volley
    # OHHV = 7 # overhead half-volley
    # OHGS = 8 # overhead ground stroke