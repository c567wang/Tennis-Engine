from shot_enums import Hand, Spin, Window

class Shot():
    """
    different kinds of shots classified by hand used, spin, pace etc.
    """
    
    def __init__(self,shot_settings,tile_dim, 
                 hand: Hand, spin: Spin, 
                 pre_bounce_pace: float, 
                 setup_time: float,
                 acc_windows: [Window], 
                 shot_risk: float, 
                 run_penalty: float,
                 min_net_dis: int,
                 static_range: [(int,int)],
                 running_range: [(int,int)]):
        self.hand = hand
        self.spin = spin
        self.pre_bounce_pace = pre_bounce_pace/tile_dim.length
        self.setup_time = setup_time
        self.acc_windows = acc_windows # e.g. some shots can't be hit from V
        self.shot_risk = shot_risk
        # run penalty synonymous with shot risk
        # if 1 then the shot can't be hit on the run
        self.run_penalty = run_penalty
        self.running_setup_time = setup_time*(1-run_penalty)
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

class ForehandFlatGroundstroke(Shot):
    """
    settings code: fhfgs
    """
    def __init__(self,shot_settings,tile_dim):
        super().__init__(shot_settings,tile_dim,
                         hand=Hand.FOREHAND,
                         spin=Spin.FLAT,
                         pre_bounce_pace=shot_settings.pace_fhfgs,
                         setup_time=shot_settings.settim_fhfgs,
                         acc_windows=[Window.EV,Window.V,Window.HV,Window.GS],
                         shot_risk=shot_settings.risk_fhfgs,
                         run_penalty=shot_settings.rp_fhfgs,
                         min_net_dis=shot_settings.mnd_fhfgs,
                         static_range=[],
                         running_range=[])
        # dummy ranges change out asap
        for i in range(5):
            for j in range(13):
                self.static_range.append((-20+i,-7+j))
        for i in range(3):
            for j in range(4):
                self.running_range.append((-18+i,1+j))
        
class BackhandDropVolley(Shot):
    """
    settings code: bhdv
    """
    def __init__(self,shot_settings,tile_dim):
        super().__init__(shot_settings,tile_dim,
                         hand=Hand.BACKHAND,
                         spin=Spin.BACKSPIN,
                         pre_bounce_pace=shot_settings.pace_bhdv,
                         setup_time=shot_settings.settim_bhdv,
                         acc_windows=[Window.EV,Window.V,Window.HV,Window.GS],
                         shot_risk=shot_settings.risk_bhdv,
                         run_penalty=shot_settings.rp_bhdv,
                         min_net_dis=shot_settings.mnd_bhdv,
                         # dummy ranges change out asap
                         static_range=[],
                         running_range=[])
        # dummy ranges change out asap
        for i in range(3):
            for j in range(7):
                self.static_range.append((1-i,2+j))