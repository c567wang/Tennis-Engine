from functions import (
        get_valid_moves,
        risk_aggr, 
        determine_windows,
        flip_windows,
        flip_player,
        flip_coordinates,
        shot_direction,
        sigmoid
)

class Node():
    # will need function generate children that calls get_valid_moves
    
    def __init__(self,windows,shot,anchor,
                 p1,p2,grid,court_settings,risk_settings,
                 bp_pos,bp_des,tp_pos,tp_des,direc,
                 window_type=None,turn=1,running=0,
                 parent=None,depth=0,risk=0):
        """
        The players whose move it is, ie the children come from their move,
        is always seen as in the bottom court. Overall the two players are
        designated p1 and p2. 1 and -1 for turn are used respectively to indicate 
        whose move/turn the node is now looking at. This player is always seen
        as being in the bottom court and referred to with bp (bottom player).
        So if turn=1, it is p1's turn to react, p1 is the bp
           if turn=-1, it is p2's turn to react, p2 is the bp
        window_type is what window the top court player hit at, None means serve
        """
        
        self.parent = parent
        self.turn = turn
        self.running = running
        self.windows = windows
        self.direc = direc
        self.bp_pos = bp_pos
        self.bp_des = bp_des
        self.tp_pos = tp_pos
        self.tp_des = tp_des
        self.depth = depth
        self.risk = risk
        self.window_type = window_type
        self.p1 = p1
        self.p2 = p2
        self.grid = grid
        self.court_settings = court_settings
        self.risk_settings = risk_settings
        
        # additional attributes only used to assess risk
        self.shot_type = shot
        self.anchor = anchor
        # net risk, dir_change risk, prev_shot_spin not implemented yet
        
        # children and risk must be length num_children
        self.num_children = 0
        self.children = []
        self.winning = False # indicator for winning position, i.e. no valid children
        # note this means this node is a winner for tp, not bp whose turn it is!!
        
    def generate_children(self):
        # sets self.winning to True if no children are generated
       
        if self.turn==0: 
            bp = self.p1
            tp = self.p2
        else:
            bp = self.p2
            tp = self.p1
            
        # get moves
        bp.pos = self.bp_pos
        bp.destination = self.bp_des
        bp.react(bp.reaction_time)
        moves = get_valid_moves(bp,self.windows,self.grid)
        if not moves: # no valid moves, the current node is a winner for tp
            self.winning = True
            return
        
        # make moves into children nodes
        # for children nodes, the current tp will become bp,
        # react has to be called for them before additional flipping/movement
        #   tp.pos = self.tp_pos
        #   tp.destination = self.tp_des
        #   tp.react(bp.reaction_time)
        #   flip_player(tp)
        for move in moves:
            
            # get risk and keep move if under tolerance
            new_direc = shot_direction(move["shot impact"],move["shot anchor"])
            dir_change = self.direc==new_direc
            move_risk = risk_aggr(self.risk_settings,move["shot impact"],
                                  move["shot anchor"],move["shot type"].id,
                                  self.shot_type.spin,dir_change,
                                  move["running"],move["window"])
            # if move_risk > 0: continue # don't necessarily want this cutoff
            
            tp.pos = self.tp_pos
            tp.destination = self.tp_des
            tp.react(move["time elapsed"])
            flip_player(tp)
            child_windows = determine_windows(move["shot type"],
                                              move["shot impact"],
                                              move["shot anchor"],
                                              self.court_settings,
                                              move["running"])
            flip_windows(child_windows)
            child = Node(windows=child_windows,
                         shot=move["shot type"],
                         anchor=move["shot anchor"],
                         p1=self.p1,
                         p2=self.p2,
                         grid=self.grid,
                         court_settings=self.court_settings,
                         risk_settings=self.risk_settings,
                         bp_pos=tp.pos,
                         bp_des=tp.destination,
                         tp_pos=flip_coordinates(move["new pos"]),
                         tp_des=flip_coordinates(move["new des"]),
                         direc=new_direc,
                         window_type=move["window"],
                         turn=-self.turn,
                         running=move["running"],
                         parent=self,
                         depth=self.depth+1,
                         risk=sigmoid(move_risk))
            self.children.append(child)
            self.num_children += 1
    
    def number_descendants(self):
        # number of total descendants obtained through recursion
        
        if not self.children:
            return 0
        sum = 0
        for child in self.children:
            sum += child.number_descendants()
        return self.num_children+sum
    
    def prune_duplicate_winners(self):
        # If a node is a winner, than it doesn't matter where the player
        # of the winner chooses as destination afterwards.
        # Calling this on a node thus gets rid of those destination-duplicates
        # This method cannot be called, for example in full_tree(), when the
        # children of a node are still being looped through
        # I.e. Make sure to call it when you are NOT looping through list of children!
        pass
    
    def examine(self):
        # print contents of node for examination
        
        print("--------")
        print("winner (if applicable):",end=" ")
        if self.turn==1:
            print("p2")
        else:
            print("p1")
        print("shot:",end=" ")
        print(self.shot_type)
        print("anchor:",end=" ")
        print(self.anchor)
        print("window:",end=" ")
        print(self.window_type)
        print("destination:",end=" ")
        print(self.tp_des)
        print("running?",end=" ")
        print(self.running)
        print("risk:",end=" ")
        print(self.risk)
        print("--------")