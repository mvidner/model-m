import math

from extended_network_model import STATES
from sklearn.metrics import mean_squared_error, mean_absolute_error


def model_rmse(model, y_true):
    infected_count = model.model.get_state_count(STATES.I_d).values[1:]
    return math.sqrt(mean_squared_error(y_true, infected_count))


def model_mae(model, y_true):
    infected_count = model.model.get_state_count(STATES.I_d).values[1:]
    return mean_absolute_error(y_true, infected_count)


return_func_zoo = {
    'rmse': model_rmse,
    'mae': model_mae
}