"""
Contains classes Court, UniformGrid
"""

import numpy as np
from scipy.interpolate import interp1d
from math import ceil

class Court():
    """
    tennis court containing dimensions
    """
    
    def __init__(self, court_dim):
        self.net_to_service_line = court_dim.net_to_service_line
        self.service_line_to_baseline = court_dim.service_line_to_baseline
        self.baseline_to_fence = court_dim.baseline_to_fence
        self.centre_service_line_to_sideline = court_dim.centre_service_line_to_sideline
        self.sideline_to_net_post = court_dim.sideline_to_net_post
        self.sideline_to_fence = court_dim.sideline_to_fence
        self.net_post_height = court_dim.net_post_height
        self.centre_net_height = court_dim.centre_net_height
        
class UniformGrid():
    """
    uniform grid generated with respect to court
    represented as:
    1. matrix with values denoting tile's in-bounds percentage:
        1: completely in-bounds
        (0,1): partially in-bounds
        0: out-of-bounds
    values change depending on if grid is set to serve/rally state
    exception: values on edge of matrix, i.e. grid[0,:], grid[:,0]
    will be percentage of grid that exists
    2. vector with length set to grid width, containing height of net (m)
    takes the interpolated parabola's tile midpoint value
    """
    
    def __init__(self, court, tile_dim, court_settings):
        # public attributes: grid; net_vec; std_dis
        #   state (0 - serve, 1 - rally, 2 - custom, grid kept as public,
        #   but best to use method when manually changing values, which
        #   will change state attribute to 2);
        #   commonly-used grid indices:
        #   (start and end refer to left to right and up to down:
        #   width-sideline-start[widx_slstart], width_sideline-end[widx_slend],
        #   length-baseline-start[lidx_blstart], length_baseline-end[lidx_blend],
        #   length-service-line-start[lidx_serstart], length-service-line-end[l_serend],
        #   width-centre[widx_centre],length-centre[lidx_centre],
        #   centre referring to the first tile after the centre point);
        #   values for partially in-bound tiles:
        #   (area-on-baseline[area_bl], area-on-baseline-sideline-intersection [area_blsl],
        #   area-on-service-line[area_serl], area-on-sideline[area_sl],
        #   area-on-service-line-sideline-intersection[area_serlsl])
        
        # grid matrix
        # initialized in serve state by calling set_serve_state
        l_partition = divmod(court.net_to_service_line + \
                             court.service_line_to_baseline + \
                             court.baseline_to_fence,tile_dim.length)
        half_l = int(l_partition[0])
        if l_partition[1]!=0:
            # court not cleanly partitioned wrt length
            half_l += 1
        w_partition = divmod(court.centre_service_line_to_sideline + \
                             court.sideline_to_fence,tile_dim.width)
        half_w = int(w_partition[0])
        if w_partition[1]!=0:
            # court not cleanly partitioned wrt width
            half_w += 1
        # lower-right quarter of grid
        q_grid = np.zeros((half_l,half_w))
        # initialize edge/outer values
        q_grid[:,(half_w-1)] = w_partition[1] / tile_dim.width
        q_grid[(half_l-1),:] = l_partition[1] / tile_dim.length
        if w_partition[1]!=0:
            if l_partition[1]!=0:
                q_grid[(half_l-1),(half_w-1)] *= w_partition[1]/tile_dim.width
            else:
                q_grid[(half_l-1),(half_w-1)] += w_partition[1]/tile_dim.width
        self.grid = np.block([
                    [np.flip(q_grid),np.flipud(q_grid)],
                    [np.fliplr(q_grid),q_grid]
                ])
        # commonly used indices (beginning from 0)
        self.widx_slstart = int((court.sideline_to_fence-w_partition[1]) \
                                //tile_dim.width) + (w_partition[1]>0)
        self.widx_centre = int(self.grid.shape[1]/2)
        self.widx_slend = int((court.sideline_to_fence + \
                               2*court.centre_service_line_to_sideline - \
                               w_partition[1]) // tile_dim.width) + (w_partition[1]>0)
        self.lidx_blstart = int((court.baseline_to_fence-l_partition[1])// \
                                tile_dim.length) + (l_partition[1]>0)
        self.lidx_centre = int(self.grid.shape[0]/2)
        self.lidx_blend = int((court.baseline_to_fence + \
                               2*court.service_line_to_baseline + \
                               2*court.net_to_service_line-l_partition[1]) // \
                               tile_dim.length) + (l_partition[1]>0)
        self.lidx_serstart = int((court.baseline_to_fence + \
                                  court.service_line_to_baseline - \
                                  l_partition[1]) // \
                                  tile_dim.length) + (l_partition[1]>0)
        self.lidx_serend = int((court.baseline_to_fence + \
                                court.service_line_to_baseline +
                                2*court.net_to_service_line - l_partition[1]) // \
                                tile_dim.length) + (l_partition[1]>0)
        # values for partially-in-bound tiles
        self.area_bl = (court.service_line_to_baseline + \
                        court.net_to_service_line)%tile_dim.length
        self.area_bl /= tile_dim.length
        self.area_sl = court.centre_service_line_to_sideline%tile_dim.width
        self.area_sl /= tile_dim.width
        self.area_blsl = self.area_bl*self.area_sl
        self.area_serl = court.net_to_service_line%tile_dim.length
        self.area_serl /= tile_dim.length
        self.area_serlsl = self.area_serl*self.area_sl
        
        self.state = 0
        self.set_serve_state()
        
        # net vector        
        self.net_vec = np.zeros((1,2*half_w))
        # interpolating quadratic polynomial
        net_f = interp1d(
                np.array([court.sideline_to_fence-\
                          court.sideline_to_net_post,
                          court.sideline_to_fence+\
                          court.centre_service_line_to_sideline,
                          court.sideline_to_fence+\
                          2*court.centre_service_line_to_sideline+\
                          court.sideline_to_net_post]),
                np.array([court.net_post_height,
                          court.centre_net_height,
                          court.net_post_height]),
                kind='quadratic')
        # get number of tiles that the net doesn't reach (on one side)
        
        no_net_num = int((court.sideline_to_fence - \
                          court.sideline_to_net_post - \
                          w_partition[1])//tile_dim.width)
        x = (no_net_num+1/2)*tile_dim.width + w_partition[1] # input to net_f
        if w_partition[1]!=0:
            no_net_num += 1
        n = self.net_vec.shape[1]-2*no_net_num # number of tiles with net
        for i in range(n):
            try:
                self.net_vec[0,no_net_num+i] = net_f(x)
            except:
                self.net_vec[0,no_net_num+i] = court.net_post_height
            x += tile_dim.width
            
        # distance (in tiles) of a player and where they hit the ball
        # included here since once the distance is fixed in meters,
        # this is a property of the grid
        self.std_dis = ceil(court_settings.std_dis/tile_dim.width-0.5)
    
    def set_serve_state(self) -> None:
        # sets grid to serve state
        # i.e. outer tiles not modified,
        # tiles on service lines and sidelines set to percentages
        # tiles inside service line and baseline set to 1
        # other tiles set to 0
        l,w = self.grid.shape
        self.grid[1:(l-1),1:(w-1)] = 0
        self.grid[(self.lidx_serstart+1):self.lidx_serend,
                  [self.widx_slstart,self.widx_slend]] = self.area_sl
        self.grid[[self.lidx_serstart,self.lidx_serend],
                  (self.widx_slstart+1):self.widx_slend] = self.area_serl
        self.grid[[[self.lidx_serstart],[self.lidx_serend]],
                  [self.widx_slstart,self.widx_slend]] = self.area_serlsl
        self.grid[(self.lidx_serstart+1):self.lidx_serend,
                  (self.widx_slstart+1):self.widx_slend] = 1
        self.state = 0
    
    def set_rally_state(self) -> None:
        # sets grid to rally state
        # i.e. outer tiles not modified,
        # tiles on baselines and sidelines set to percentages
        # tiles completely in-bounds set to 1
        # other tiles set to 0
        l,w = self.grid.shape
        self.grid[1:(l-1),1:(w-1)] = 0
        self.grid[(self.lidx_blstart+1):self.lidx_blend,
                  [self.widx_slstart,self.widx_slend]] = self.area_sl
        self.grid[[self.lidx_blstart,self.lidx_blend],
                  (self.widx_slstart+1):self.widx_slend] = self.area_bl
        self.grid[[[self.lidx_blstart],[self.lidx_blend]],
                  [self.widx_slstart,self.widx_slend]] = self.area_blsl
        self.grid[(self.lidx_blstart+1):self.lidx_blend,
                  (self.widx_slstart+1):self.widx_slend] = 1
        self.state = 1
    
    def custom_grid_value(self, x, y, val) -> None:
        # change grid value at (x,y) to val
        # state attribute set to 2
        self.grid[x,y] = val
        self.state = 2
    
    def serve_in(self, x, y) -> (bool, None):
        if self.state!=1:
            return self.grid[x,y] > 0
        else:
            print("Grid not in serving state.")
            return
    
    def ball_in(self, x, y) -> (bool, None):
        if self.state!=0:
            return self.grid[x,y] > 0
        else:
            print("Grid not in rally state.")
            return
    
    def get_tile_risk(self, x, y) -> float:
        l,w = self.grid.shape
        # check if on border of entire court
        if x!=0 and x!=(l-1) and y!=0 and y!=(w-1):
            return 1-self.grid[x,y]
        else:
            # in which case definitely out
            return 1