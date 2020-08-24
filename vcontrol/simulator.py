import numpy as np

from .vessels import Vessel
from .controllers import PIDController
from typing import Tuple, List, Callable
import matplotlib.pyplot as plt


class Simulator:
    def __init__(self, t_0: float = 0):
        self.t_0 = t_0
        self._time_line = []

    def reset(self):
        for vessel in Vessel.get_instances():
            vessel.reset()

    def simulate_to_t(self, t: float, dt: float):
        self.reset()
        self._time_line = np.arange(self.t_0, t, dt)
        for _ in self._time_line:
            for i, vessel in enumerate(Vessel.get_instances()):
                vessel.update_height(dt)
            for vessel in Vessel.get_instances():
                vessel.update_control(dt)

    def plot(self, time_range: Tuple[float, float] = None):

        def get_time_line_and_ranger() -> Tuple[np.ndarray, Callable[[List], np.ndarray]]:
            """
            Im sorry for this ( ཀ ʖ̯ ཀ)
            """
            if time_range:
                time_line = np.array(self._time_line)
                r_min, r_max = time_range
                index_map = (r_min <= time_line) & (self._time_line <= r_max)

                def time_ranged(arr: List) -> np.ndarray:
                    arr = np.array(arr)
                    return arr[index_map]
                return time_line[index_map], time_ranged

            return np.array(self._time_line), lambda x: x

        time_line, time_ranged = get_time_line_and_ranger()
        fig, axs = plt.subplots(3, len(list(Vessel.get_instances())),
                                sharex='col', sharey='row',
                                gridspec_kw={'hspace': 0, 'wspace': 0})
        (axs_h, axs_o, axs_q) = axs
        for i, vessel in enumerate(Vessel.get_instances()):
            if vessel.name:
                axs_h[i].set_title(f'{vessel.name}', fontsize=18)
            else:
                axs_h[i].set_title(f'Tank {i}', fontsize=18)

            o = time_ranged(np.maximum(np.minimum(vessel.history['output'], 1.0), 0.0))
            axs_h[i].plot(time_line, time_ranged(vessel.history['h']), color='green', lw=1.5)
            if isinstance(vessel.drain_control, PIDController):
                axs_h[i].axhline(y=vessel.drain_control.set_point, color='red', ls='--')

            axs_o[i].plot(time_line, o, color='blue', lw=1.5)
            axs_q[i].plot(time_line, time_ranged(vessel.history['Q']), color='red', lw=1.5)

            for ax in [axs_h[i], axs_o[i], axs_q[i]]:
                ax.grid(b=True, which='major', color='#999999', linestyle='-')
                ax.minorticks_on()
                ax.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(1.5)

            axs_q[i].set_xlabel('t', fontsize=18)
            if i == 0:
                axs_h[i].set_ylabel('Water Level', fontsize=18)
                axs_o[i].set_ylabel('Controller Output', fontsize=18)
                axs_q[i].set_ylabel('Water Outflow', fontsize=18)

        return fig, (axs_h, axs_o, axs_q)

