"""
Set-up file used for other tests

Sets up the two players and their shots, the court grid,
and initializes the two players positions and destinations.
"""

from settings import (
        CourtDim, 
        TileDim,
        CourtSettings,
        PlayerSettings, 
        ShotSettings
)
from court_grid import Court, UniformGrid
from shots import *
from shot_enums import Window as W
from player import Player
from player_enums import CourtHalf as CH
from functions import get_valid_moves
import numpy as np # why are the window values numpy arrays again?

# court-grid initialization
court_dim = CourtDim()
tile_dim = TileDim()
court_settings = CourtSettings()
court = Court(court_dim)
grid = UniformGrid(court,tile_dim,court_settings)

# initial input window for testing
initial_windows = {W.V: np.array([(19,9),0.2]),
                  W.HV: np.array([(24,10),0.7]),
                  W.GS: np.array([(28,11),1])}

# shot initialization
shot_settings = ShotSettings()
fhfgs = ForehandFlatGroundstroke(shot_settings,tile_dim)
bhdv = BackhandDropVolley(shot_settings,tile_dim)

# player initialization
player_settings = PlayerSettings()
p1 = Player(player_settings,tile_dim,court_half=CH.TOP)
p1.pos = (8,7)
p1.destination = (12,7)
p1.left_shots = [fhfgs]
p1.right_shots = [bhdv]
p1.update_shots()
p2 = Player(player_settings,tile_dim,court_half=CH.BOTTOM)
p2.pos = (28,10)
p2.destination = (28,10)
p2.left_shots = [fhfgs]
p2.right_shots = [bhdv]
p2.update_shots()

# moves for p2
# p1,p2 reacts to p1's move first
p2.react(p2.reaction_time)
p1.react(p2.reaction_time)
res = get_valid_moves(p2,p1,initial_windows,grid) # test passed, microseconds