##### SETUP #####  
# Running play_setup first!
from play_setup import play_setup
p1,p2,grid,court_settings,risk_settings,\
initial_windows,initial_anchor,initial_direc,\
kick,flat,tpsn,uarm,fhtgs,bhtgs,fhfgs,bhfgs,\
fhdv,bhdv,fhlob,bhlob,fhsl,bhsl,smash,tweener = play_setup()
#################

# play_setup comes with initial p1, p2, serve
# toggle the serve and the players' positions/destinations/arsenals as needed here:
# p2.destination = (8,10)
# p1.pos = (32,10)
# p1.destination = (32,10)
# p2.speed = 100 # purely for testing

from node import Node

def full_tree(cur_node,depth:int):
    """
    Uses recursion to generate brute force full game tree at specified depth
    starting from the cur_node
    Goes to depth+1 to detect winners + assess risk to obtain initial evals
    (that can then be weighed with risk)
    
    Uses a global winner list to collect winners that can then be traced by parent
    """
    
    cur_node.generate_children()
    if cur_node.winning:
        winners.append(cur_node)
        return
    if depth==0:
        return
    for child in cur_node.children:
        full_tree(child,depth-1)
        
def negamax(cur_node,p2_serve=True):
    """
    Given tree extending from cur_node, implements naive negamax starting
    from all leaf nodes, uses recursion
    """
    
    if not cur_node.children:
        if cur_node.winning:
            return -cur_node.turn
        else:
            return 0
    if p2_serve:
        if cur_node.depth%2==0: # current depth is even, P1 is looking to maximize
            return max(negamax(c,p2_serve)*(1-c.risk)-cur_node.turn*c.risk
                       for c in cur_node.children)
        else: # current depth is odd, P2 is looking to minimize
            return min(negamax(c,p2_serve)*(1-c.risk)-cur_node.turn*c.risk
                       for c in cur_node.children)
    else:
        if cur_node.depth%2==0:
            return min(negamax(c,p2_serve)*(1-c.risk)-cur_node.turn*c.risk
                       for c in cur_node.children)
        else:
            return max(negamax(c,p2_serve)*(1-c.risk)-cur_node.turn*c.risk
                       for c in cur_node.children)
  
d = 2 # depth      
winners = []
service_node = Node(windows=initial_windows,
                    shot=kick,
                    anchor=initial_anchor,
                    p1=p1,p2=p2,grid=grid,
                    court_settings=court_settings,risk_settings=risk_settings,
                    bp_pos=p1.pos,bp_des=p1.destination,
                    tp_pos=p2.pos,tp_des=p2.destination,direc=initial_direc)
full_tree(service_node,depth=d)
# get unique list of moves
move_wo_des = [] # moves without destination (shot type + anchor)
unique_winners = []
for w in winners:
    if (w.shot_type,w.anchor) not in move_wo_des:
        unique_winners.append(w)
        move_wo_des.append((w.shot_type,w.anchor))
e = negamax(service_node)