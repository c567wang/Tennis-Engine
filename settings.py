# all distance in meters, all time in seconds
import math

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
        # Horizontal speed retained
        # The ratio of the horizontal speed after the bounce to the horizontal
        # speed before the bounce doesn’t have a special name because it 
        # depends on the angle of incidence. In the above example, the ratio 
        # is 42/70 = 0.60. On a fast court the ratio is usually a bit higher 
        # and on a slow court the ratio can be lower, but in practice, the 
        # ratio is usually between 0.4 and 0.75 on all courts and at all angles
        # of incidence of practical interest. - PTT
        self.hsr = 0.6
        
        # COR - coefficient of restitution
        # - deprecated after trajectory script (it is used there)
        # “The COR is reasonably constant for a given court, 
        # regardless of the ball speed or the angle of incidence. 
        # However, it can vary on an uneven or patchy surface like grass. 
        # On grass courts, the ball doesn’t bounce as well, and the 
        # COR is about 0.7, but it depends on which patch of grass the ball 
        # hits and whether the grass is new or worn. Values of the COR as 
        # high as 0.9 have been observed on some grass surfaces and also on 
        # hard court surfaces, particularly at low angles of incidence.” - PTT
        # self.cor = 0.8
        
        # topspin distance reduction - deprecated after trajectory script
        # a ball with topspin will fly less further horizontally than it would
        # have if it had no topspin, we approximate this with a scalar
        # self.tdr = 0.9
        
        # standard distance between player and ball upon impact in meters
        # not taking into account hand used
        self.std_dis = 1
        
        # drag coefficient
        self.c_d = 0.5
        # air density
        self.rho = 1.21
        # ball radius
        self.r = 0.0325
        # ball mass
        self.m = 0.057
        # k coefficient
        self.k = self.rho*math.pi*self.r**2/(2*self.m)
        # gravity acceleration
        self.g = 9.8
        
class ServeSettings():
    
    def __init__(self):
        
        # pre-bounce pace (pace)
        self.pace_kick = 33 # 40
        self.pace_flat = 40 # 47
        self.pace_tpsn = 33.5 # 42
        self.pace_uarm = 22
        
class ShotSettings():
    """
    metrics and adjustable attributes for various shots
    shot ranges (static & running) are hardcoded directly in shots.py
    """
    
    def __init__(self):
        
        # pre-bounce pace (pace)        
        # forehand topspin groundstroke
        self.pace_fhtgs = 29
        # backhand topspin groundstroke
        self.pace_bhtgs = 28
        # forehand flat groundstroke
        self.pace_fhfgs = 32
        # backhand flat groundstroke
        self.pace_bhfgs = 31
        # forehand drop volley
        self.pace_fhdv = 4.5
        # backhand drop volley
        self.pace_bhdv = 4.5
        # forehand lob
        self.pace_fhlob = 17.5
        # backhand lob
        self.pace_bhlob = 17.5
        # forehand slice
        self.pace_fhsl = 12
        # backhand slice
        self.pace_bhsl = 12
        # overhead smash
        self.pace_smash = 47
        # tweener
        self.pace_tweener = 17
        
        # setup times (settim)
        # forehand topspin groundstroke
        self.settim_fhtgs = 0.2
        # backhand topspin groundstroke
        self.settim_bhtgs = 0.25
        # forehand flat groundstroke
        self.settim_fhfgs = 0.2
        # backhand flat groundstroke
        self.settim_bhfgs = 0.25
        # forehand drop volley
        self.settim_fhdv = 0.2
        # backhand drop volley
        self.settim_bhdv = 0.2
        # forehand lob
        self.settim_fhlob = 0.05
        # backhand lob
        self.settim_bhlob = 0.05
        # forehand slice
        self.settim_fhsl = 0.5
        # backhand slice
        self.settim_bhsl = 0.55
        # overhead smash
        self.settim_smash = 0.55
        # tweener
        self.settim_tweener = 0.3
        
        # minimum net distance (in terms of tiles) (mnd)
        # forehand topspin groundstroke
        self.mnd_fhtgs = 1
        # backhand topspin groundstroke
        self.mnd_bhtgs = 1
        # forehand flat groundstroke
        self.mnd_fhfgs = 2
        # backhand flat groundstroke
        self.mnd_bhfgs = 2
        # forehand drop volley
        self.mnd_fhdv = 0
        # backhand drop volley
        self.mnd_bhdv = 0
        # forehand lob
        self.mnd_fhlob = 0
        # backhand lob
        self.mnd_bhlob = 0
        # forehand slice
        self.mnd_fhsl = 0
        # backhand slice
        self.mnd_bhsl = 0
        # overhead smash
        self.mnd_smash = 0
        # tweener
        self.mnd_tweener = 2
        
class PlayerSettings():
    """
    adjustable metrics for the average player
    """
    
    def __init__(self):
        self.reaction_time = 0.37 # seconds
        self.halting_time = 0.4 # seconds
        self.speed = 4.5 # m/s

class ShotRiskSettings():
    """
    shot risk coefficients obtained through regression
    """
    
    def __init__(self):
        self.baseline = -1 # beta0 in regression
        
        self.tile_baseline = 0.2 # id 2 in data
        self.tile_sideline = 0.3 # id 3 in data
        self.tile_corner = 0.4 # id 4 in data
        self.running = 0.35
        self.net = 0.2 # hitting from middle lane to non middle lane
        self.window_ev = 0.3 # baseline is groundstroke
        self.window_v = 0.2
        self.window_hv = 0.1
        self.dir_change = 0.2
        
        # shot execution risk (baseline forehand topspin groundstroke)
        self.fhtgs = 0.1
        self.bhtgs = 0.15
        self.fhfgs = 0.3
        self.bhfgs = 0.32
        self.fhdv = 0.1
        self.bhdv = 0.15
        self.fhlob = 0
        self.bhlob = 0.05
        self.fhsl = 0.25
        self.bhsl = 0.3
        self.smash = 0.15
        self.tweener = 0.6
        
        # run penalty risk (baseline forehand topspin groundstroke)
        self.rp_fhtgs = 0.3
        self.rp_bhtgs = 0.4
        self.rp_fhfgs = 0.25
        self.rp_bhfgs = 0.3
        self.rp_fhdv = 0.5
        self.rp_bhdv = 0.6
        self.rp_fhlob = 0
        self.rp_bhlob = 0
        self.rp_fhsl = 0.8
        self.rp_bhsl = 0.9
        self.rp_smash = 0.3
        self.rp_tweener = 0.9
        self.rp_std = max(self.rp_fhtgs,self.rp_bhtgs,self.rp_fhfgs,self.rp_bhfgs,
                     self.rp_fhdv,self.rp_bhdv,self.rp_fhlob,self.rp_bhlob,
                     self.rp_fhsl,self.rp_bhsl,self.rp_smash,self.rp_tweener)+0.5
        
        # previous shot spin (baseline topspin)
        self.prev_t = 0 # topspin baseline
        self.prev_f = 0.25 # flat
        self.prev_b = 0.3 # backspin