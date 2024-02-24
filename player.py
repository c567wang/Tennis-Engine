from player_enums import DominantHand as DH

class Player():
    
    def __init__(self,player_settings,tile_dim,court_half,hand=DH.RIGHT):
        self.hand = hand
        self.half = court_half # only where they start as perspective flips
        self.speed = player_settings.speed/tile_dim.length
        self.reaction_time = player_settings.reaction_time
        self.halting_time = player_settings.halting_time
        self.pos = (0,0)
        # speed translated in terms of tiles/second
        # only works for square tiles for now
        self.destination = (0,0)
        # list of shots that they can make
        # the program that fills these lists has to use
        # half and hand attr of the player and the shot's hand attr
        # with left/middle/right referring to *player relative to impact tile*
        # e.g. for a right-handed player playing top court,
        # ForehandFlatGroundstroke would go into left_shots
        # NEW: with the court perspective changing shot-to-shot,
        # the player we are concerned with will always be in bottom court
        self.left_shots = []
        self.middle_shots = []
        self.right_shots = []
        self.shots = [self.left_shots,self.middle_shots,self.right_shots]
    
    """
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
    """
        
    def update_shots(self):
        # call everytime after manual tinkering with left/middle/right_shots
        self.shots = [self.left_shots,self.middle_shots,self.right_shots]