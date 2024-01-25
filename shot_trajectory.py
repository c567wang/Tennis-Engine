import numpy as np
from functions import (
        determine_impact_tile
)
from player_enums import CourtHalf as CH
from shot_enums import Window as W

class ShotTrajectory():
    """
    trajectory of a shot encoded as matrix of arrival times
    """
    
    def __init__(self, grid, shot, player):
        l,w = grid.grid.shape
        l2 = int(l/2) # first row where opponent court starts
        self.times = np.zeros((l,w))
        # determine impact position
        # possibly replace in future with passing xstart, ystart directly
        xstart, ystart = determine_impact_tile(shot, player)
        windows = shot.determine_windows()
        # Direction based on CH
        for window in windows:
            info = window.values()
            self.times[xstart+info[0],ystart+info[1]]
            
            
            # EV = 1 # early volley
            # V = 2 # volley
            # HV = 3 # half-volley
            # GS = 4 # ground stroke