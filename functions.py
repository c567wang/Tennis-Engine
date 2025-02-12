import math
import operator
import numpy as np

# functions arranged alphabetically
# passed/TODO: left_handed_ranges
# needs refining: 

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
    
def determine_windows(shot, impact, anchor, cs, running=False):
    """
    Makes use of shot's spin and pre-bounce speed to calculate shot trajectory
    given the coordinates for impact and anchor. The window coordinates
    and their arrival times are then extracted and return in a dict
    cs is court settings in settings.py where hsr,k,c_d are found
    Output format: {window:Window: np.array([(x:int,y:int),time:float])}
    Sample output: {Window.V: np.array([(15,10),1.05]),
                    Window.GS: np.array([(7,11),3])}
    Invalid windows, often EV and sometimes V, are simply excluded
    !! Function is always working with impact in bottom half of court !!
    """
    
    ret = {}
    direc = tuple(map(operator.sub,anchor,impact))
    
    # EV - early volley
    direc_ev = tuple(round(i*shot.window_fractions[0]) for i in direc)
    ev = tuple(map(operator.add,impact,direc_ev))
    if ev[0] < 18:
        dist = math.sqrt(direc_ev[0]**2+direc_ev[1]**2)
        if running:
            t = time_to_x(cs.k,cs.c_d,shot.running_pace,dist)
        else:
            t = time_to_x(cs.k,cs.c_d,shot.pre_bounce_pace,dist)
        ret[0] = np.array([ev,t])
    
    # V - volley
    direc_v = tuple(round(i*shot.window_fractions[1]) for i in direc)
    v = tuple(map(operator.add,impact,direc_v))
    if v[0] < 18:
        dist = math.sqrt(direc_v[0]**2+direc_v[1]**2)
        if running:
            t = time_to_x(cs.k,cs.c_d,shot.running_pace,dist)
        else:
            t = time_to_x(cs.k,cs.c_d,shot.pre_bounce_pace,dist)
        ret[1] = np.array([v,t])    
    
    # post-bounce ball: get time for pre_bounce, apply hsr
    dist_pre = math.sqrt(direc[0]**2+direc[1]**2)
    t_pre = time_to_x(cs.k,cs.c_d,shot.pre_bounce_pace,dist_pre)
    
    # HV - half volley
    direc_hv = tuple(round(i*shot.window_fractions[2]) for i in direc)
    if (shot.spin==4): # kick serve
        direc_hv = tuple(map(operator.add,direc_hv,(0,1))) # shift to right by 1
    hv = tuple(map(operator.add,anchor,direc_hv))
    dist = math.sqrt(direc_hv[0]**2+direc_hv[1]**2)
    if running:
        t = time_to_x(cs.k,cs.c_d,cs.hsr*shot.running_pace,dist) + t_pre
    else:
        t = time_to_x(cs.k,cs.c_d,cs.hsr*shot.pre_bounce_pace,dist) + t_pre
    ret[2] = np.array([hv,t])
    
    # GS - ground stroke
    direc_gs = tuple(round(i*shot.window_fractions[3]) for i in direc)
    if (shot.spin==4): # kick serve
        direc_gs = tuple(map(operator.add,direc_gs,(0,1))) # shift to right by 1
    gs = tuple(map(operator.add,anchor,direc_gs))
    dist = math.sqrt(direc_gs[0]**2+direc_gs[1]**2)
    if running:
        t = time_to_x(cs.k,cs.c_d,cs.hsr*shot.running_pace,dist) + t_pre
    else:
        t = time_to_x(cs.k,cs.c_d,cs.hsr*shot.pre_bounce_pace,dist) + t_pre
    ret[3] = np.array([gs,t])
    
    # delete out of bound ranges
    pop = []
    for i in ret.keys():
        if ret[i][0][0] < 0 or ret[i][0][1] < 0 or ret[i][0][0] > 35:
            pop.append(i)
    for i in pop:
        ret.pop(i,None)
    
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

def flip_player(p):
    """
    Flips the direction the program sees the entire court (including players)
    so get_valid_moves etc. only have to calculate for player residing on
    the lower half of the court after this function is called
    Items flipped: Player positions, destinations
    """
    
    p.pos = flip_coordinates(p.pos)
    p.destination = flip_coordinates(p.destination)
        
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

def get_valid_moves(player,windows,grid):
    """
    Returns list of moves, a move is a list in the following order
    
    a dict with the following keys:
        {"shot type","shot impact","shot anchor","new pos","new dest","running"}
    player: Player
    windows: Dict with shot trajectory information
    grid: UniformGrid
    
    Important: The function does not mutate any player or window
    It takes into account the player's reaction time wrt the windows,
    BOTH PLAYER AND OPPONENT'S POS/DESTINATION NEED TO BE UPDATED MANUALLY
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
        reachable[window,2] = reachable[window,1] - t_right
        reachable[window,1] = reachable[window,1] - t_middle
    
    # print(reachable)
            
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
                    if shot.std_run_penalty<1 and \
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
                              "new des":dest,
                              "running":choice["running"],
                              "window":choice["window"],
                              "time elapsed":windows[choice["window"]][1]})
    return moves

def left_handed_ranges(shot_range):
    """
    Takes list of relative coordinates shot_range and flips along the y-axis
    for use of left-handed players, as all the ranges are hardcoded for 
    right-handers. This function ideally used during initialization of model
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
    cos = (vec[0]*new[0]+vec[1]*new[1])/math.sqrt((vec[0]**2+vec[1]**2)+(new[0]**2+new[1]**2))
    if cos >= 0:
        return 0
    else:
        k = 0.16
        return -k*cos

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
    ret = [player_pos,(l,7),(l,10)] # staying put, cheating to ad/deuce
    if w < 7:
        w0 = 7
    elif w > 10:
        w0 = 10
    else:
        w0 = w
    ret.extend([(19,w0),(29,w0),(32,w0)]) # moving to net/baseline/deep
    ret = list(set(ret)) # get rid of duplicates
    return ret
    
def risk_aggr(risk_settings,impact,anchor,shot_id,
              par_spin,dir_change,running,window):
    """
    function aggregating all risk factors
    """
    
    risk = risk_settings.baseline
    # tile risk
    if anchor[0]==6:
        if anchor[1]==4 or anchor[1]==13:
            risk += risk_settings.tile_corner
        else:
            risk += risk_settings.tile_baseline
    elif anchor[1]==4 or anchor[1]==13:
        risk += risk_settings.tile_sideline
    # add line below since only 0.115 of our 1x1 sideline tiles contain
    # area that is "in", so their adjacent tiles also carry risk to a lesser degree
    elif anchor[1]==5 or anchor[1]==12:
        risk += risk_settings.tile_sideline*0.5
    # net risk
    if 6 < impact[1] < 11 and (anchor[1]<7 or anchor[1]>10):
        risk += risk_settings.net
    # previous shot spin (add if flat or backspin)
    if par_spin==0:
        risk += risk_settings.prev_f
    elif par_spin==2:
        risk += risk_settings.prev_b
    # window risk
    if window==0:
        risk += risk_settings.window_ev
    elif window==1:
        risk += risk_settings.window_v
    elif window==2:
        risk += risk_settings.window_hv
    # change-of-direction risk
    if dir_change: risk += risk_settings.dir_change
    # running risk
    if running: risk += risk_settings.running
    # shot risk & interaction term with running
    if shot_id==1:
        risk += risk_settings.fhtgs
        if running: risk += risk_settings.rp_fhtgs
    if shot_id==2:
        risk += risk_settings.bhtgs
        if running: risk += risk_settings.rp_bhtgs
    if shot_id==3:
        risk += risk_settings.fhfgs
        if running: risk += risk_settings.rp_fhfgs
    if shot_id==4:
        risk += risk_settings.bhfgs
        if running: risk += risk_settings.rp_bhfgs
    if shot_id==5:
        risk += risk_settings.fhdv
        if running: risk += risk_settings.rp_fhdv
    if shot_id==6:
        risk += risk_settings.bhdv
        if running: risk += risk_settings.rp_bhdv
    if shot_id==7:
        risk += risk_settings.fhlob
        if running: risk += risk_settings.rp_fhlob
    if shot_id==8:
        risk += risk_settings.bhlob
        if running: risk += risk_settings.rp_bhlob
    if shot_id==9:
        risk += risk_settings.fhsl
        if running: risk += risk_settings.rp_fhsl
    if shot_id==10:
        risk += risk_settings.bhsl
        if running: risk += risk_settings.rp_bhsl
    if shot_id==11:
        risk += risk_settings.smash
        if running: risk += risk_settings.rp_smash
    if shot_id==12:
        risk += risk_settings.tweener
        if running: risk += risk_settings.rp_tweener
        
    return risk
    
def shot_direction(start,end):
    """
    returns one of intenums DTL(0),CCL(1),CCLX(2),CCR(3),CCRX(4);
    always looking at court from perspective of bottom half player
    """
    
    if end[1] < start[1]-4:
        return 2
    elif end[1] < start[1]-1:
        return 1
    elif end[1] < start[1]+2:
        return 0
    elif end[1] < start[1]+5:
        return 3
    else:
        return 4
    
def sigmoid(x):
    return 1/(1+math.exp(-x))
    
def time_to_pt(player,pt):
    """
    returns time for player to get to the exact coordinates given pt
    """
    
    t = distance_between(pt,player.pos)/player.speed
    t += movement_readjust_penalty(player,pt)
    return t

def time_to_x(k,c_d,v0,x):
    """
    returns time taken for ball to travel horizontal distance x
    given initial pace v0
    """
    
    t = (math.exp(k*c_d*x)-1)/(k*c_d*v0)
    return t