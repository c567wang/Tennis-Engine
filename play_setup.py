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
        ShotSettings,
        ServeSettings,
        ShotRiskSettings
)
from court_grid import Court, UniformGrid
from shots import *
from serves import *
from player import Player
from player_enums import CourtHalf as CH
from functions import (
        determine_windows, 
        shot_direction,
        flip_coordinates,
        flip_windows
)

def play_setup():
    
    # court-grid initialization
    court_dim = CourtDim()
    tile_dim = TileDim()
    court_settings = CourtSettings()
    risk_settings = ShotRiskSettings()
    court = Court(court_dim)
    grid = UniformGrid(court,tile_dim,court_settings)
    
    """
    # initial input window for testing
    initial_windows = {W.V: np.array([(19,9),0.2]),
                       W.HV: np.array([(24,10),0.7]),
                       W.GS: np.array([(28,11),1])}
    """
    
    # shot initialization
    shot_settings = ShotSettings()
    fhtgs = ForehandTopspinGroundstroke(shot_settings,risk_settings,tile_dim)
    bhtgs = BackhandTopspinGroundstroke(shot_settings,risk_settings,tile_dim)
    fhfgs = ForehandFlatGroundstroke(shot_settings,risk_settings,tile_dim)
    bhfgs = BackhandFlatGroundstroke(shot_settings,risk_settings,tile_dim)
    fhdv = ForehandDropVolley(shot_settings,risk_settings,tile_dim)
    bhdv = BackhandDropVolley(shot_settings,risk_settings,tile_dim)
    fhlob = ForehandLob(shot_settings,risk_settings,tile_dim)
    bhlob = BackhandLob(shot_settings,risk_settings,tile_dim)
    fhsl = ForehandSlice(shot_settings,risk_settings,tile_dim)
    bhsl = BackhandSlice(shot_settings,risk_settings,tile_dim)
    smash = OverheadSmash(shot_settings,risk_settings,tile_dim)
    tweener = Tweener(shot_settings,risk_settings,tile_dim)
    # serve initialization
    serve_settings = ServeSettings()
    kick = KickServe(serve_settings)
    flat = FlatServe(serve_settings)
    tpsn = TopspinServe(serve_settings)
    uarm = UnderarmServe(serve_settings)
    
    # player initialization
    player_settings = PlayerSettings()
    p2 = Player(player_settings,tile_dim,court_half=CH.TOP)
    p2.pos = (6,10)
    p2.destination = (6,10)
    p2.left_shots = [fhtgs,fhfgs,fhdv,fhlob,fhsl]
    p2.middle_shots = [smash,tweener]
    p2.right_shots = [bhtgs,bhfgs,bhdv,bhlob,bhsl]
    p2.update_shots()
    p2.serves = [kick,flat,tpsn,uarm]
    p1 = Player(player_settings,tile_dim,court_half=CH.BOTTOM)
    p1.pos = (32,6)
    p1.destination = (32,4)
    p1.left_shots = [fhtgs,fhfgs,fhdv,fhlob,fhsl]
    p1.middle_shots = [smash,tweener]
    p1.right_shots = [bhtgs,bhfgs,bhdv,bhlob,bhsl]
    p1.update_shots()
    p2.serves = [kick,flat,tpsn,uarm]
    
    initial_anchor = (21,6)
    # note for serves impact tile can be inside service line,
    # players are lunging forward as they serve
    initial_windows = determine_windows(kick,
                                        flip_coordinates(p2.pos),
                                        flip_coordinates(initial_anchor),
                                        court_settings)
    flip_windows(initial_windows)
    initial_direc = shot_direction(flip_coordinates(p2.pos),
                                   flip_coordinates(initial_anchor))
    
    return (p1,p2,grid,court_settings,risk_settings,
            initial_windows,initial_anchor,initial_direc,
            kick,flat,tpsn,uarm,
            fhtgs,bhtgs,fhfgs,bhfgs,
            fhdv,bhdv,fhlob,bhlob,
            fhsl,bhsl,smash,tweener)
# -----------------------------------------------------------------------------
# moves for p2
# p1,p2 reacts to p1's move first
# p2.react(p2.reaction_time)
# p1.react(p2.reaction_time)
# res = get_valid_moves(p2,p1,initial_windows,grid) # test passed, microseconds
# win = determine_windows(bhdv, (21,7),(14,10),court_settings)