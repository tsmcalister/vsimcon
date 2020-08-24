from typing import Tuple
from .simulator import Simulator
from .vessels.vessel import Vessel

__version__ = "0.0.1"

# reset on import
_SIMULATOR = Simulator()


def simulate(to_t: float, dt: float):
    """
    Simulate the system up to time to_t
    :param to_t: time limit of the simulation
    :param dt: the time step used in the simulation
    """
    _SIMULATOR.simulate_to_t(to_t, dt)


def reset():
    """
    Resets all Vessel instances to exclude them from simulation
    """
    Vessel.reset_instances()


def plot(time_range: Tuple[float, float] = None):
    return _SIMULATOR.plot(time_range)
