import math

from extended_network_model import STATES
from sklearn.metrics import mean_squared_error


def model_rmse(model, y_true):
    infected_count = model.model.get_state_count(STATES.I_d).values
    res = math.sqrt(mean_squared_error(y_true, infected_count))
    print(res)
    return res


return_func_zoo = {
    'rmse': model_rmse
}