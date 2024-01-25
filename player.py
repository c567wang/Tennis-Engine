from player_enums import (
        MovementState as MS,
        DominantHand as DH,
        CourtHalf as CH
)
from settings import(
        PlayerSettings as PS,
        TileDim as TD
)
import operator

# speed from settings

class Player():
    
    def __init__(self, speed, half: CH, hand=DH.RIGHT):
        self.hand = hand
        self.half = half
        self.reaction_time = PS.reaction_time
        self.halting_time = PS.halting_time
        self.pos = (0,0)
        # not the player's speed at some given time
        # speed translated in terms of tiles/second
        # only works for square tiles for now
        self.speed = speed/TD.length
        self.destination = (0,0)
        # list of shots that they can make
        # the program that fills these lists has to use
        # half and hand attr of the player and the shot's hand attr
        # with left/middle/right referring to impact tile relative to player
        # e.g. for a right-handed player playing top court,
        # ForehandFlatGroundstroke would go into left_shots
        self.left_shots = []
        self.middle_shots = []
        self.right_shots = []
        self.shots = [self.left_shots,self.middle_shots,self.right_shots]
    
    def get_movement_state(self):
        vec = tuple(map(operator.sub,
                        self.destination,
                        self.pos))
        if vec == (0,0):
            return MS.SPLITSTEP
        elif sum(vec) < 2:
            return MS.SLIDE
        else:
            return MS.SPRINT
        
    def update_shots(self):
        self.shots = [self.left_shots,self.middle_shots,self.right_shots]