import math
import operator
import numpy as np

# functions arranged alphabetically
# passed/TODO: net_risk, risk_aggr, left_handed_ranges
# needs refining: determine_windows

def coord_shift(coord,direction,d):
    """
    Takes coordinate tuple coord - (x,y)
    returns (x,y-d) if direction is "left"
    returns (x,y+d) if direction is "right"
    note may return invalid tile if there is no tile in direction
    i.e. if coord is on the very edge of the extended court
    """
    
    if direction=="left":
        return tuple(map(operator.sub,coord,(0,d)))
    elif direction=="right":
        return tuple(map(operator.add,coord,(0,d)))
    else:
        return coord
    
def determine_windows(shot, impact, anchor, cs):
    """
    Makes use of shot's spin and pre-bounce speed to calculate shot trajectory
    given the coordinates for impact and anchor. The window coordinates
    and their arrival times are then extracted and return in a dict
    cs is court settings in settings.py where cof/cor/tdr are found
    Output format: {window:Window: np.array([(x:int,y:int),time:float])}
    Sample output: {Window.V: np.array([(15,10),1.05]),
                    Window.GS: np.array([(7,11),3])}
    Invalid windows, often EV and sometimes V, are simply excluded
    """
    # incredibly simplistic version not factoring in spin for testing purposes
    # translate pre-bounce speed into tiles, take 30% off post bounce 
    # in same direction and windows to be roughly half way points
    
    ret = {}
    direc = tuple(map(operator.sub,anchor,impact))
    
    # EV - early volley
    direc_ev = tuple(round(i/5) for i in direc)
    ev = tuple(map(operator.add,impact,direc_ev))
    if ev[0] < 18:
        dist = math.sqrt(direc_ev[0]**2+direc_ev[1]**2)
        t = dist/shot.pre_bounce_pace
        ret[0] = np.array([ev,t])
    
    # V - volley
    direc_v = tuple(round(4*i/5) for i in direc)
    v = tuple(map(operator.add,impact,direc_v))
    if v[0] < 18:
        dist = math.sqrt(direc_v[0]**2+direc_v[1]**2)
        t = dist/shot.pre_bounce_pace
        ret[1] = np.array([v,t])    
    
    # post-bounce ball: 1) accumulates topspin (tdr applied
    #                       and windows taken closer to center of trajectory)
    #                   2) horizontal speed decreases (by factor cof)
    #                   3) vertical speed decreases (distance reduced by
    #                       COF*sqrt(COR) relative to direc)
    reduce_direc = cs.cof*math.sqrt(cs.cor)*cs.tdr
    dist_pre = math.sqrt(direc[0]**2+direc[1]**2)
    t_pre = dist_pre/shot.pre_bounce_pace
    
    # HV - half volley
    direc_hv = tuple(round(reduce_direc*i/3) for i in direc)
    hv = tuple(map(operator.add,anchor,direc_hv))
    dist = math.sqrt(direc_hv[0]**2+direc_hv[1]**2)
    t = dist/(cs.cof*shot.pre_bounce_pace) + t_pre
    ret[2] = np.array([hv,t])
    
    # GS - ground stroke
    direc_gs = tuple(round(reduce_direc*i*3/5) for i in direc)
    gs = tuple(map(operator.add,anchor,direc_gs))
    dist = math.sqrt(direc_gs[0]**2+direc_gs[1]**2)
    t = dist/(cs.cof*shot.pre_bounce_pace) + t_pre
    ret[3] = np.array([gs,t])
    
    return(ret)
    
def distance_between(pt1, pt2):
    """
    pt1,2 are 2d tuples
    """
    return math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)

def flip_coordinates(coord):
    """
    Helper for flip_court_perspective below
    Does flipping for only one coordinate, hardcoded
    """
    
    return tuple(map(operator.sub,(35,17),coord))

def flip_players(p1,p2):
    """
    Flips the direction the program sees the entire court (including players)
    so get_valid_moves etc. only have to calculate for player residing on
    the lower half of the court after this function is called
    Items flipped: Player positions, destinations
    """
    
    p1.pos = flip_coordinates(p1.pos)
    p1.destination = flip_coordinates(p1.destination)
    p2.pos = flip_coordinates(p2.pos)
    p2.destination = flip_coordinates(p2.destination)
        
def flip_windows(windows):
    """
    Flips the coordinates of the windows so that where before they were going
    from the bottom court to the top court, now they are going from the top
    court to the bottom court, and further evaluation get_valid_moves can
    be called with these windows
    
    windows: one single Dict of windows with at most four elements (EV,V,HV,GS)
    """
    
    for window in windows.keys():
        windows[window][0] = flip_coordinates(windows[window][0])

def get_valid_moves(player,opponent,windows,grid):
    """
    Returns list of moves, a move is a list in the following order
    
    a dict with the following keys:
        {"shot type","shot impact","shot anchor","new pos","new dest"}
    player, opponent: Player
    windows: Dict with shot trajectory information
    grid: UniformGrid
    
    Important: The function does not mutate any player or window
    It takes into account the player's reaction time wrt the windows,
    but BOTH PLAYER AND OPPONENT'S POS/DESTINATION NEED TO BE UPDATED MANUALLY
    BY THE PROGRAM CALLING THIS FUNCTION
    """
    
    # function is getting moves for player
    # designated player B in comments
    # while opponent is designated player A
    # function looks at court from perspective of B being in bottom-half
    
    # 1. What is the state of the game after B reacts?
    # As mentioned in function description, this function no longer updates
    # player positions. The program calling should do this!!!
    reachable = np.zeros((4,3)) # explained in (2) below
    for window in windows.keys():
        reachable[window,1] = windows[window][1] - player.reaction_time
    
    # 2. For a given window, can B get there in time?
    # results returned in 4x3 matrix
    #   | L | M | R
    # EV|
    # V | remaining time if reachable
    # HV| negative => not reachable
    # GS| 0 => reachable but need to hit running
    # as noted in Player.py, direction (left/middle/right) refers to
    # player position relative to impact tile
    # e.g. bottom-court right-handed forehand is left
    for window in windows.keys():
        # window is type IntEnum so used as index here
        # window position is windows[window][0]
        middle = windows[window][0]
        left = coord_shift(middle,"left",grid.std_dis)
        right = coord_shift(middle,"right",grid.std_dis)
        t_left = time_to_pt(player,left)
        t_middle = time_to_pt(player,middle)
        t_right = time_to_pt(player,right)
        reachable[window,0] = reachable[window,1] - t_left
        reachable[window,1] = reachable[window,1] - t_middle
        reachable[window,2] = reachable[window,1] - t_right
        
    print(reachable)
            
    # 3. Which shots does the remaining set-up time allow? 
    #    and in what state would the player be hitting
    # pass information from step 3 to step 4 json-esqe
    shot_choices = []
    side = ["left","middle","right"]
    for i in range(4):
        for j in range(3):
            if reachable[i,j]>player.halting_time:
                # halting and set-up can happen at the same time
                # hitting in split-step state
                for shot in player.shots[j]:
                    if reachable[i,j]>=shot.setup_time and \
                    i in shot.acc_windows:
                        choice = {"window":i,
                                  "side":side[j],
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
                                  "side":side[j],
                                  "running":1,
                                  "type":shot
                                 }
                        shot_choices.append(choice)
    # 3.5 TODO: extra step here or in loop below to filter down
    # shot selections based on prior shot, e.g. dropshot => non topspin return
    
    # 4. For each remaining shot, which tiles serve as valid anchors?
    # 5. Which tiles make sense to start moving towards?
    moves = []
    for choice in shot_choices:
        shot = choice["type"]
        window = windows[choice["window"]][0] # window tile coordinates
        anchor_incr = shot.running_range if choice["running"] else shot.static_range
        p_pos = coord_shift(window,choice["side"],grid.std_dis) # player pos if hit shot
        new_dest = new_destinations(p_pos)
        anchors = [tuple(map(operator.add,window,incr)) for incr in anchor_incr]
        for anchor in list(anchors): # list for copy as will be removing items
            # if anchor coord out of bounds, remove
            if anchor[0] < grid.lidx_blstart or anchor[0] >= grid.lidx_centre or \
            anchor[1] < grid.widx_slstart or anchor[1] > grid.widx_slend:
                anchors.remove(anchor)
                continue
            # if anchor not reachable because of net, remove
            if grid.lidx_centre-anchor[0] < choice["type"].min_net_dis:
                anchors.remove(anchor)
                continue
        for anchor in anchors:
            for dest in new_dest:
                moves.append({"shot type":shot,
                              "shot impact":window,
                              "shot anchor":anchor,
                              "new pos":p_pos,
                              "new dest":dest})
    return moves

def left_handed_ranges(shot_range):
    """
    Takes list of relative coordinates shot_range and flips along the y-axis
    for use of left-handed players, as all the ranges are hardcoded for 
    right-handers. Ideally used during initialization of model
    """
    pass

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
    
def net_risk(start,anchor,grid):
    pass

def new_destinations(player_pos):
    """
    returns list of coordinate options to set as new destination for player
    right after hitting the ball (player_pos is coordinate tuple)
    according to set running rules;
    dependent (for now) only on where a player is on the court;
    assumes player to be on the bottom-half court;
    hard-coded wrt initial grid
    """
    
    l,w = player_pos
    ret = []
    ret.extend([(l,7),(l,8),(l,9),(l,10)])
    if w < 7:
        w0 = 7
    elif w > 10:
        w0 = 10
    else:
        w0 = w
    ret.extend([(18,w0),(23,w0),(28,w0),(29,w0),(30,w0),(31,w0)])
    ret = list(set(ret))
    return ret
    
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