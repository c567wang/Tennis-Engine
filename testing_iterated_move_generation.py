"""
Several tests for basic functions needed for iterated move generation
(flip_players, determine_windows, flip_windows), aims to get idea of runtime

Copy-pastes testing_play_setup first instead of using exec
"""

##### testing_play_setup WITH ADDITIONAL IMPORTS #####

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
from functions import (
        get_valid_moves, 
        flip_players, 
        flip_windows, 
        determine_windows
)
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
d1_moves = get_valid_moves(p2,p1,initial_windows,grid) # test passed, microseconds 

##### END OF COPY-PASTE #####

## TEST 1: CALLING determine_windows ON ALL MOVES IN d1_moves
## incredibly quick, also less than one second

"""
windows = []
for move in d1_moves:
    w = determine_windows(move[0],move[1],move[2], court_settings)
    windows.append(w)
"""
    
## TEST 2: CALLING flip_players, determine_windows, flip_windows
## still incredibly quick, seemingly with no bugs, problem is no viable moves
## for p1 can be found (they are high up the court)

"""
move = d1_moves[7]
# after move is determined we know where p2 is and where they are going 
# after those are updated react makes sense
p2.pos = move["new pos"]
p2.destination = move["new dest"]
p2.react(p1.reaction_time)
p1.react(p1.reaction_time)
flip_players(p1,p2)
windows = determine_windows(move["shot type"],
                            move["shot impact"],
                            move["shot anchor"],
                            court_settings)
flip_windows(windows)
"""

## TEST 3: ITERATING TO DEPTH 2
## Under it's original speed, very quick (microseconds) but no viable moves
## Artifically set forehand ground stroke speed to 10 instead of 31.9
## slower, around 1 second, with 305658 nodes
## depth 3 may be limit for brute force

d2_moves = [] # list of lists
winners = [] # d1 moves that p1 has no response to
p1.react(p1.reaction_time) # p1 can react, p2's choice of move irrelevant
# will need original coordinates to reset
old_pos = p2.pos
old_dest = p2.destination
for move in d1_moves:
    p2.pos = move["new pos"]
    p2.destination = move["new dest"]
    p2.react(p1.reaction_time)
    flip_players(p1,p2)
    windows = determine_windows(move["shot type"],
                            move["shot impact"],
                            move["shot anchor"],
                            court_settings)
    flip_windows(windows)
    d2_move = get_valid_moves(p1,p2,windows,grid)
    if d2_move: 
        d2_moves.append(d2_move)
    else:
        winners.append(move)
    # reset 
    # TODO: a better way (?) would be to flip all the new pos/dest for p2
    # so we don't have to flip the board twice per d1 move
    # though as of now it doesn't seem like flipping is too expensive
    flip_players(p1,p2)
    p2.pos = old_pos
    p2.destination = old_dest
    
## TEST 4: AD-HOC SANDBOX
move = winners[9]
p2.pos = move["new pos"]
p2.destination = move["new dest"]
p2.react(p1.reaction_time)
p1.react(p1.reaction_time)
flip_players(p1,p2)
windows = determine_windows(move["shot type"],
                            move["shot impact"],
                            move["shot anchor"],
                            court_settings)
flip_windows(windows)