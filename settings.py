# all distance in meters, all time in seconds

class CourtDim():
    """
    all dimensions for the court
    """
    
    def __init__(self):
        
        # length
        self.net_to_service_line = 6.401
        self.service_line_to_baseline = 5.486
        self.baseline_to_fence = 5.486
        # width
        self.centre_service_line_to_sideline = 4.115
        self.sideline_to_net_post = 0.914
        self.sideline_to_fence = 4.420
        # height
        self.net_post_height = 1.067
        self.centre_net_height = 0.914

class TileDim():
    """
    dimensions for tiles overlaying court
    default is 1x1
    """
    
    def __init__(self):    
        # grid uniform for now
        self.length = 1
        self.width = 1
        
class CourtSettings():
    """
    """
    
    def __init__(self):
        # COF - coefficient of friction
        # usually 0.6 for fast courts like grass,
        # 0.7 for slow courts like clay, 0.7 otherwise
        self.cof = 0.7
        
        # standard distance between player and ball upon impact in meters
        # not taking into account hand used
        self.std_dis = 1
        
class ShotSettings():
    """
    metrics and adjustable attributes for various shots
    shot ranges (static & running) are hardcoded directly in shots.py
    """
    
    def __init__(self):
        
        # pre-bounce pace (pace)
        # forehand flat ground stroke
        self.pace_fhfgs = 31.9 # WEB ARTICLES
        # backhand drop volley
        self.pace_bhdv = 5 # NOT SOURCED
        
        # setup times (settim)
        # forehand flat ground stroke
        self.settim_fhfgs = 0.5 # NOT SOURCED
        # backhand drop volley
        self.settim_bhdv = 0.3 # NOT SOURCED
        
        # shot risk/difficulty/control/accuracy (between 0 and 1)
        # forehand flat ground stroke
        self.risk_fhfgs = 0.5 # NOT SOURCED
        # backhand drop volley
        self.risk_bhdv = 0.6 # NOT SOURCED
        
        # shot running penalty (rp, between 0 and 1)
        # forehand flat ground stroke
        self.rp_fhfgs = 0.3 # NOT SOURCED
        # backhand drop volley
        self.rp_bhdv = 0.5 # NOT SOURCED
        
        # minimum net distance (in terms of tiles) (mnd)
        # forehand flat ground stroke
        self.mnd_fhfgs = 1 # NOT SOURCED
        # backhand drop volley
        self.mnd_bhdv = 0 # STANDARD ASSUMPTION
        
class PlayerSettings():
    """
    adjustable metrics for the average player
    """
    
    def __init__(self):
        self.reaction_time = 0.15 # seconds
        self.halting_time = 0.15 # seconds
        self.speed = 4 # m/s, sourced but need to revisit