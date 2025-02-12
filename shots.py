from shot_enums import Hand, Spin, Window

class Shot():
    """
    different kinds of shots classified by hand used, spin, pace etc.
    """
    
    def __init__(self,shot_settings,risk_settings,
                 tile_dim, hand: Hand, spin: Spin, 
                 pre_bounce_pace: float, 
                 setup_time: float,
                 acc_windows: [Window], 
                 shot_risk: float, 
                 run_penalty: float,
                 min_net_dis: int,
                 static_range: [(int,int)],
                 running_range: [(int,int)],
                 window_fractions: [int], # windows (IntEnums) are indices
                 idx): # id for shot
        self.id = idx
        self.hand = hand
        self.spin = spin
        self.pre_bounce_pace = pre_bounce_pace/tile_dim.length
        self.setup_time = setup_time
        self.acc_windows = acc_windows # e.g. some shots can't be hit from V
        self.shot_risk = shot_risk
        # run penalty synonymous with shot risk
        # if 1 then the shot can't be hit on the run
        self.run_penalty = run_penalty
        self.std_run_penalty = run_penalty/risk_settings.rp_std
        self.running_setup_time = setup_time*(1-self.std_run_penalty)
        self.running_pace = self.pre_bounce_pace*max((1-self.std_run_penalty),0.5)
        # hardcoding shot range in terms of tiles relative to window
        # instead of translating depth, angles into tiles
        # shot range represented by list of anchors (relative to window coord)
        # get_valid_moves assumes hitting from bottom half to top half
        # so x-coordinates will be negative 
        self.static_range = static_range
        self.running_range = running_range # most probably a subset of self.range
        # minimum distance of tiles needed for anchor to be from net for the 
        # shot to be feasible (can be 0); hardcoded as well 
        self.min_net_dis = min_net_dis

class ForehandTopspinGroundstroke(Shot):
    """
    settings code: fhtgs
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.FOREHAND,
                         spin=Spin.TOPSPIN,
                         pre_bounce_pace=shot_settings.pace_fhtgs,
                         setup_time=shot_settings.settim_fhtgs,
                         acc_windows=[Window.EV,Window.V,Window.HV,Window.GS],
                         shot_risk=risk_settings.fhtgs,
                         run_penalty=risk_settings.rp_fhtgs,
                         min_net_dis=shot_settings.mnd_fhtgs,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=1)
        self.static_range = [(-21,-2),(-21,-1),(-21,0),(-21,1),
                             (-20,-3),(-20,-2),(-20,-1),(-20,0),(-20,1),(-20,2),
                             (-19,-4),(-19,-3),(-19,-2),(-19,-1),(-19,0),(-19,1),(-19,2),
                             (-18,-3),(-18,-2),(-18,-1),(-18,0),(-18,1)]
        self.running_range = [(-18,-2),(-18,-1),(-18,0)]
        self.window_fractions = [0.16, 0.84, 0.19, 0.41]
    
    def __str__(self):
        return "Forehand Topspin Groundstroke"
        
class BackhandTopspinGroundstroke(Shot):
    """
    settings code: bhtgs
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.BACKHAND,
                         spin=Spin.TOPSPIN,
                         pre_bounce_pace=shot_settings.pace_bhtgs,
                         setup_time=shot_settings.settim_bhtgs,
                         acc_windows=[Window.EV,Window.V,Window.HV,Window.GS],
                         shot_risk=risk_settings.bhtgs,
                         run_penalty=risk_settings.rp_bhtgs,
                         min_net_dis=shot_settings.mnd_bhtgs,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=2)
        self.static_range = [(-19,-1),(-19,0),(-19,1),(-19,2),
                             (-18,-2),(-18,-1),(-18,0),(-18,1),(-18,2),(-18,3),
                             (-17,-2),(-17,-1),(-17,0),(-17,1),(-17,2),(-17,3),(-17,4),
                             (-16,-1),(-16,0),(-16,1),(-16,2),(-16,3)]
        self.running_range = [(-16,0),(-16,1),(-16,2)]
        self.window_fractions = [0.17, 0.83, 0.2, 0.41]
        
    def __str__(self):
        return "Backhand Topspin Groundstroke"

class ForehandFlatGroundstroke(Shot):
    """
    settings code: fhfgs
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.FOREHAND,
                         spin=Spin.FLAT,
                         pre_bounce_pace=shot_settings.pace_fhfgs,
                         setup_time=shot_settings.settim_fhfgs,
                         acc_windows=[Window.EV,Window.V,Window.HV,Window.GS],
                         shot_risk=risk_settings.fhfgs,
                         run_penalty=risk_settings.rp_fhfgs,
                         min_net_dis=shot_settings.mnd_fhfgs,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=3)
        self.static_range = [(-22,-1),(-22,0),
                             (-21,-2),(-21,-1),(-21,0),(-21,1),
                             (-20,-3),(-20,-2),(-20,-1),(-20,0),(-20,1),
                             (-19,-4),(-19,-3),(-19,-2),(-19,-1),(-19,0),(-19,1),(-19,2),
                             (-18,-5),(-18,-4),(-18,-3),(-18,-2),(-18,-1),(-18,0),(-18,1)]
        self.running_range = [(-18,-4),(-18,-3),(-18,-2),(-18,-1),(-18,0)]
        self.window_fractions = [0.21, 0.89, 0.13, 0.3]
        
    def __str__(self):
        return "Forehand Flat Groundstroke"
        
class BackhandFlatGroundstroke(Shot):
    """
    settings code: bhfgs
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.BACKHAND,
                         spin=Spin.FLAT,
                         pre_bounce_pace=shot_settings.pace_bhfgs,
                         setup_time=shot_settings.settim_bhfgs,
                         acc_windows=[Window.EV,Window.V,Window.HV,Window.GS],
                         shot_risk=risk_settings.bhfgs,
                         run_penalty=risk_settings.rp_bhfgs,
                         min_net_dis=shot_settings.mnd_bhfgs,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=4)
        self.static_range = [(-20,0),(-20,1),(-20,2),
                             (-19,-1),(-19,0),(-19,1),(-19,2),(-19,3),
                             (-18,-2),(-18,-1),(-18,0),(-18,1),(-18,2),(-18,3),(-18,4),(-18,5),
                             (-17,-1),(-17,0),(-17,1),(-17,2),(-17,3),(-17,4)]
        self.running_range = [(-17,0),(-17,1),(-17,2),(-17,3)]
        self.window_fractions = [0.22, 0.89, 0.13, 0.31]
        
    def __str__(self):
        return "Backhand Flat Groundstroke"
        
class ForehandDropVolley(Shot):
    """
    settings code: fhdv
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.FOREHAND,
                         spin=Spin.FLAT,
                         pre_bounce_pace=shot_settings.pace_fhdv,
                         setup_time=shot_settings.settim_fhdv,
                         acc_windows=[Window.V,Window.GS],
                         shot_risk=risk_settings.fhdv,
                         run_penalty=risk_settings.rp_fhdv,
                         min_net_dis=shot_settings.mnd_fhdv,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=5)
        self.static_range = [(-4,-1),(-4,0),(-4,1),
                             (-3,-1),(-3,0),(-3,1),
                             (-2,-1),(-2,0),(-2,1)]
        self.running_range = [(-3,0)]
        self.window_fractions = [0.11, 0.91, 0.1, 0.62]
        
    def __str__(self):
        return "Forehand Drop Volley"
        
class BackhandDropVolley(Shot):
    """
    settings code: bhdv
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.BACKHAND,
                         spin=Spin.FLAT,
                         pre_bounce_pace=shot_settings.pace_bhdv,
                         setup_time=shot_settings.settim_bhdv,
                         acc_windows=[Window.V,Window.GS],
                         shot_risk=risk_settings.bhdv,
                         run_penalty=risk_settings.rp_bhdv,
                         min_net_dis=shot_settings.mnd_bhdv,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=6)
        self.static_range = [(-4,-1),(-4,0),(-4,1),
                             (-3,-1),(-3,0),(-3,1),
                             (-2,-1),(-2,0),(-2,1)]
        self.running_range = [(-3,0)]
        self.window_fractions = [0.11, 0.91, 0.1, 0.62]
        
    def __str__(self):
        return "Backhand Drop Volley"
        
class ForehandLob(Shot):
    """
    settings code: fhlob
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.FOREHAND,
                         spin=Spin.TOPSPIN,
                         pre_bounce_pace=shot_settings.pace_fhlob,
                         setup_time=shot_settings.settim_fhlob,
                         acc_windows=[Window.V,Window.GS],
                         shot_risk=risk_settings.fhlob,
                         run_penalty=risk_settings.rp_fhlob,
                         min_net_dis=shot_settings.mnd_fhlob,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],idx=7)
        self.static_range = [(-26,0),
                             (-25,0),
                             (-24,0),
                             (-23,0),
                             (-22,0),
                             (-21,0),
                             (-20,0),
                             (-19,0)]
        self.running_range = [(-26,0),
                              (-25,0),
                              (-24,0),
                              (-23,0)]
        self.window_fractions = [0.01, 0.98, 0.02, 0.33]
        
    def __str__(self):
        return "Forehand Lob"
        
class BackhandLob(Shot):
    """
    settings code: bhlob
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.BACKHAND,
                         spin=Spin.TOPSPIN,
                         pre_bounce_pace=shot_settings.pace_bhlob,
                         setup_time=shot_settings.settim_bhlob,
                         acc_windows=[Window.V,Window.GS],
                         shot_risk=risk_settings.bhlob,
                         run_penalty=risk_settings.rp_bhlob,
                         min_net_dis=shot_settings.mnd_bhlob,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=8)
        self.static_range = [(-26,0),
                             (-25,0),
                             (-24,0),
                             (-23,0),
                             (-22,0),
                             (-21,0),
                             (-20,0),
                             (-19,0)]
        self.running_range = [(-26,0),
                              (-25,0),
                              (-24,0),
                              (-23,0)]
        self.window_fractions = [0.01, 0.98,0.02, 0.33]
        
    def __str__(self):
        return "Backhand Lob"
        
class ForehandSlice(Shot):
    """
    settings code: fhsl
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.FOREHAND,
                         spin=Spin.BACKSPIN,
                         pre_bounce_pace=shot_settings.pace_fhsl,
                         setup_time=shot_settings.settim_fhsl,
                         acc_windows=[Window.V,Window.GS],
                         shot_risk=risk_settings.fhsl,
                         run_penalty=risk_settings.rp_fhsl,
                         min_net_dis=shot_settings.mnd_fhsl,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=9)
        self.static_range = [(-15,-1),(-15,0),(-15,1),(-15,2),
                             (-14,-1),(-14,0),(-14,1),(-14,2),
                             (-13,-1),(-13,0),(-13,1),(-13,2)]
        self.running_range = [(-15,0),(-15,1),(-15,2),
                              (-14,0),(-14,1),(-14,2),
                              (-13,0),(-13,1),(-13,2)]
        self.window_fractions = [0.03, 0.94, 0.06, 0.41]
        
    def __str__(self):
        return "Forehand Slice"
        
class BackhandSlice(Shot):
    """
    settings code: bhsl
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.BACKHAND,
                         spin=Spin.BACKSPIN,
                         pre_bounce_pace=shot_settings.pace_bhsl,
                         setup_time=shot_settings.settim_bhsl,
                         acc_windows=[Window.V,Window.GS],
                         shot_risk=risk_settings.bhsl,
                         run_penalty=risk_settings.rp_bhsl,
                         min_net_dis=shot_settings.mnd_bhsl,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=10)
        self.static_range = [(-15,-2),(-15,-1),(-15,0),(-15,1),
                             (-14,-2),(-14,-1),(-14,0),(-14,1),
                             (-13,-2),(-13,-1),(-13,0),(-13,1)]
        self.running_range = [(-15,-2),(-15,-1),(-15,0),
                              (-14,-2),(-14,-1),(-14,0),
                              (-13,-2),(-13,-1),(-13,0)]
        self.window_fractions = [0.03, 0.94, 0.06, 0.41]
        
    def __str__(self):
        return "Backhand Slice"
        
class OverheadSmash(Shot):
    """
    settings code: smash
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.CENTERED,
                         spin=Spin.FLAT,
                         pre_bounce_pace=shot_settings.pace_smash,
                         setup_time=shot_settings.settim_smash,
                         acc_windows=[Window.EV,Window.V,Window.GS],
                         shot_risk=risk_settings.smash,
                         run_penalty=risk_settings.rp_smash,
                         min_net_dis=shot_settings.mnd_smash,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=11)
        self.static_range = [(-6,-2),(-6,-1),(-6,0),(-6,1),(-6,2),
                             (-5,-3),(-5,-2),(-5,-1),(-5,0),(-5,1),(-5,2),(-5,3),
                             (-4,-2),(-4,-1),(-4,0),(-4,1),(-4,2),
                             (-3,-1),(-3,0),(-3,1)]
        self.running_range = [(-4,-1),(-4,0),(-4,1)]
        self.window_fractions = [0, 0, 0.42, 16.89]
        
    def __str__(self):
        return "Overhead Smash"
        
class Tweener(Shot):
    """
    settings code: tweener
    """
    def __init__(self,shot_settings,risk_settings,tile_dim):
        super().__init__(shot_settings,risk_settings,tile_dim,
                         hand=Hand.CENTERED,
                         spin=Spin.FLAT,
                         pre_bounce_pace=shot_settings.pace_tweener,
                         setup_time=shot_settings.settim_tweener,
                         acc_windows=[Window.GS],
                         shot_risk=risk_settings.tweener,
                         run_penalty=risk_settings.rp_tweener,
                         min_net_dis=shot_settings.mnd_tweener,
                         static_range=[],
                         running_range=[],
                         window_fractions=[],
                         idx=12)
        self.static_range = [(-22,0)]
        self.running_range = [(-22,0)]
        self.window_fractions = [0, 0.82, 1.24, 1.44]
        
    def __str__(self):
        return "Tweener"