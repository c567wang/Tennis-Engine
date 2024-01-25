import math
import operator
import numpy as np
# from player_enums import (
#         DominantHand as DH,
#         CourtHalf as CH
# )
# from shot_enums import Hand, Window
# from player import Player

# functions arranged alphabetically

def coord_shift(coord,direction,d):
    """
    takes coordinate tuple coord - (x,y)
    returns (x,y-d) if direction is "left"
    returns (x,y+d) if direction is "right"
    note may return invalid tile if there is no tile in direction
    i.e. if coord is on the very edge of the extended court
    """
    
    if direction=="left":
        return tuple(map(operator.sub,coord,(0,d)))
    elif direction=="right":
        return tuple(map(operator.add,coord,(0,d)))
    
def distance_between(pt1, pt2):
    """
    pt1,2 are 2d tuples
    """
    return math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)

def get_valid_moves(player,opponent,windows,grid):
    """
    player, opponent: Player
    windows: Dict with shot trajectory information
    grid: UniformGrid
    """
    
    # function is getting moves for player
    # designated player B in comments
    # while opponent is designated player A
    
    # 1. What is the state of the game after B reacts?
    for window in windows.keys():
        windows[window][1] -= player.reaction_time
    # A moves
    opponent.pos = movement_at_t(player.reaction_time,
                                 opponent.speed,
                                 opponent.pos,
                                 opponent.destination)
    # B continues moving if they were moving prior
    player.pos = movement_at_t(player.reaction_time,
                               player.speed,
                               player.pos,
                               player.destination)
    
    
    # 2. For a given window, can B get there in time?
    # results returned in 4x3 matrix
    #   | L | M | R
    # EV|
    # V | remaining time if reachable
    # HV| negative => not reachable
    # GS| 0 => reachable but need to hit running
    reachable = np.zeros((4,3))
    for window in windows.keys():
        # window is type IntEnum so used as index here
        # window position is windows[window][0]
        middle = windows[window][0]
        left = coord_shift(middle,"left",grid.std_dis)
        right = coord_shift(middle,"right",grid.std_dis)
        t_left = time_to_pt(player,left)
        t_middle = time_to_pt(player,middle)
        t_right = time_to_pt(player,right)
        reachable[window,0] = windows[window][1] - t_left
        reachable[window,1] = windows[window][1] - t_middle
        reachable[window,2] = windows[window][1] - t_right
            
    # 3. Which shots does the remaining set-up time allow? 
    #    and in what state would the player be hitting
    # pass information from step 3 to step 4 json-esqe
    shot_choices = []
    for i in range(4):
        for j in range(3):
            if reachable[i,j]>player.halting_time:
                # halting and set-up can happen at the same time
                # hitting in split-step state
                for shot in player.shots[j]:
                    if reachable[i,j]>=shot.setup_time and \
                    i in shot.acc_windows:
                        choice = {"window":i,
                                  "side":j,
                                  "running":0,
                                  "type":shot
                                 }
                        shot_choices.append(choice)
            elif reachable[i,j]>0:
                # will have to hit the shot while running
                for shot in player.shots[j]:
                    if shot.run_penalty<1 and \
                    reachable[i,j]>=shot.running_setup_time and \
                    i in shot.acc_windows:
                        choice = {"window":i,
                                  "side":j,
                                  "running":1,
                                  "type":shot
                                 }
                        shot_choices.append(choice)
    
    # 4. For each remaining shot, which tiles serve as valid anchors?
    for choice in shot_choices:
        
    
    # 5. Which tiles make sense to start moving towards?
    
    # 4&5 - choice of tiles need to be limited, and the limitation should
    #       work for both of these as they are connected
    #       e.g. one player's run is where another player tends to hit

def movement_at_t(t, speed, start, end):
    """
    Given start and end grid coordinates for a movement,
    return what grid the player, travelling with speed speed,
    is on at time t
    Neither the player's pos or destination are changed
    """
    if start==end: return end
    
    vec = tuple(map(operator.sub,end,start))
    angle = math.atan2(vec[0],vec[1])
    distance = speed*t
    x = start[0]+math.ceil(distance*math.sin(angle)-1/2)
    x = min(end[0],x,key=abs)
    y = start[1]+math.ceil(distance*math.cos(angle)-1/2)
    y = min(end[1],y,key=abs)
    return (x,y)

def movement_readjust_penalty(player,new_destination):
    """
    Given new_destination coordinate tuple,
    decides whether penalty is needed and how much.
    For now, penalty imposed if direction player heading in and
    vector of player pos and new_destination form obtuse angle.
    If so, penalty is linear to angle with coefficient k
    """
    
    vec = tuple(map(operator.sub,player.destination,player.pos))
    if vec==(0,0): return 0
    new = tuple(map(operator.sub,new_destination,player.pos))
    # is getting cos too computationally expensive?
    cos = (vec[0]*new[0]+vec[1]*new[1])/math.sqrt((vec[0]**2+vec[1]**2)*(new[0]**2+new[1]**2))
    if cos >= 0:
        return 0
    else:
        k = 0.16
        return k*cos
    
def risk_aggr():
    """
    function aggregating all risk factors
    """
    
    pass
    
def time_to_pt(player,pt):
    """
    returns time for player to get to the exact coordinates given pt
    """
    
    t = distance_between(pt,player.pos)/player.speed
    t += movement_readjust_penalty(player,pt)
    return t