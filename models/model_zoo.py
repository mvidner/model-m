# models

# model = ENGINE + MODEL DEFINITION

# engine is not cofigurable yet
# you can specify your model definition


from seirs import SEIRSModel, SEIRSNetworkModel
from extended_network_model import ExtendedNetworkModel
from seirs_extended import ExtendedNetworkModel as OldExtendedNetworkModel

__all__ = [
    ExtendedNetworkModel,          # our extended version
    SEIRSModel,                    # original seirsplus code
    SEIRSNetworkModel,             # original seirsplus code
    OldExtendedNetworkModel        # abandonded implementation
]

model_zoo = {
    "ExtendedNetworkModel": ExtendedNetworkModel,
    "OldExtendedNetworkModel": OldExtendedNetworkModel,
    "SEIRSNetworkModel": SEIRSNetworkModel
}
