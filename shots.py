from shot_enums import Hand, Spin, Window
from player_enums import MovementState
from settings import ShotSettings as ss
# from shot_enums import Window
# from math import ceil
import numpy as np

class Shot():
    """
    different kinds of shots classified by hand used, spin, pace etc.
    """
    
    def __init__(self, hand: Hand, spin: Spin, 
                 pre_bounce_pace: float, 
                 setup_time: float, 
                 setup_state: [MovementState], 
                 acc_windows: [Window], 
                 shot_risk: float, 
                 run_penalty: float, 
                 ang_range: (float,float),
                 depth_range: (float,float),
                 tile_dim):
        self.hand = hand
        self.spin = spin
        self.pre_bounce_pace = pre_bounce_pace
        self.setup_time = setup_time
        # self.setup_state = setup_state
        self.acc_windows = acc_windows # e.g. some shots can't be hit from V
        self.shot_risk = shot_risk
        # run penalty synonymous with shot risk
        # if 1 then can't be hit on the run
        self.run_penalty = run_penalty
        self.running = 0 # binary 1/0 for yes/no
        self.running_setup_time = setup_time*(1-run_penalty)
        ## tile_dim.width needed to calculate how many grids
        ## standard distance needed translates into
        ## commenting out and moving to uniform_grid as attr instead
        ## self.std_dis = ceil(ss.std_dis/tile_dim.width-0.5)
        # translate shot ranges (angular/depth) into tiles!
        self.ang_range = ang_range # angular range of shot in cosine value
        self.depth_range = depth_range
        
    def determine_windows(self, anchor) -> {Window: np.array([(int,int),float])}:
        # arrival time and position relative to impact point for each window
        # {window: np.array([(x,y),time])} 
        # e.g. {Window.V: np.array([(15,20),1.05])}
        # invalid windows, often EV and sometimes V, will not be included
        # anchor will indicate which half of the court is being targeted
        pass
    
    def set_running(self):
        self.running = 1

class ForehandFlatGroundstroke(Shot):
    def __init__(self, pre_bounce_pace, tile_dim):
        # rework
        super().__init__(hand=Hand.FOREHAND,spin=Spin.FLAT,
             pre_bounce_pace=pre_bounce_pace, setup_time=ss.settim_fhgs,
             setup_pos=[MovementState.SLIDE,MovementState.SPLITSTEP,
                        MovementState.SPRINT], 
             shot_risk = ss.risk_fhfgs,
             # run_penalty = 
             tile_dim = tile_dim)