from functions import sigmoid, risk_aggr
from settings import ShotRiskSettings

risk_settings = ShotRiskSettings()
impact = (29,11)
anchor = (11,8)
shot_id = 1
par_spin = 0 # 0 flat; 2 backspin
dir_change = 0
running = 1
window = 3
res = sigmoid(risk_aggr(risk_settings,impact,anchor,shot_id,
                        par_spin,dir_change,running,window))