from functions import *
from settings import (
        TileDim,
        CourtSettings,
        PlayerSettings, 
        ShotSettings,
        ShotRiskSettings
)
from shots import ForehandTopspinGroundstroke, BackhandTopspinGroundstroke
from player import Player
from player_enums import CourtHalf as CH

player_settings = PlayerSettings()
tile_dim = TileDim()
shot_settings = ShotSettings()
risk_settings = ShotRiskSettings()
fhtgs = ForehandTopspinGroundstroke(shot_settings,risk_settings,tile_dim)
bhtgs = BackhandTopspinGroundstroke(shot_settings,risk_settings,tile_dim)
p = Player(player_settings,tile_dim,CH.TOP)
p.pos = (32,5) # (29,6)
p.destination = (32,5)
p.speed = 4.5 # can we get much higher?! 
wt_ar = time_to_pt(p,(33,3))+p.reaction_time
wt_lw = wt_ar+bhtgs.running_setup_time
wt_up = wt_ar+bhtgs.setup_time


court_settings = CourtSettings()
pbp = 33
# want time to be wt
t = time_to_x(court_settings.k,
              court_settings.c_d,
              pbp,distance_between((6,10),(21,6))) + \
    time_to_x(court_settings.k,
              court_settings.c_d,
              0.6*pbp,distance_between((21,6),(33,2)))