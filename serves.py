from shot_enums import Spin

class Serve():
    
    def __init__(self,
                 serve_settings,
                 pre_bounce_pace,
                 spin: Spin,
                 window_fractions: [int]):
        self.spin = spin
        self.window_fractions = window_fractions
        self.pre_bounce_pace = pre_bounce_pace
        self.run_penalty = 0 # won't be running for serve
        self.running_pace = self.pre_bounce_pace*(1-self.run_penalty)
        
class KickServe(Serve):
    """
    settings code: kick
    """
    
    def __init__(self,serve_settings):
        super().__init__(serve_settings,
                         pre_bounce_pace=serve_settings.pace_kick,
                         spin=Spin.SIDESPIN_RIGHT,
                         window_fractions=[])
        self.window_fractions = [0, 0.66, 0.42, 0.78]
        
    def __str__(self):
        return "Kick Serve"
    
class FlatServe(Serve):
    """
    settings code: flat
    """
    
    def __init__(self,serve_settings):
        super().__init__(serve_settings,
                         pre_bounce_pace=serve_settings.pace_flat,
                         spin=Spin.FLAT,
                         window_fractions=[])
        self.window_fractions = [0, 0.77, 0.33, 0.51]
        
class TopspinServe(Serve):
    """
    settings code: tpsn
    """
    
    def __init__(self,serve_settings):
        super().__init__(serve_settings,
                         pre_bounce_pace=serve_settings.pace_tpsn,
                         spin=Spin.TOPSPIN,
                         window_fractions=[])
        self.window_fractions = [0, 0.66, 0.42, 0.78]
        
class UnderarmServe(Serve):
    """
    settings code: uarm
    """
    
    def __init__(self,serve_settings):
        super().__init__(serve_settings,
                         pre_bounce_pace=serve_settings.pace_uarm,
                         spin=Spin.TOPSPIN,
                         window_fractions=[])
        self.window_fractions = [0, 0.87, 0.13, 0.53]