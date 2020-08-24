from typing import Callable
from .vessel import Vessel
from ..controllers import AbstractController, FixedController


class SourceVessel(Vessel):
    def __init__(self, flow_t: Callable[[float], float],
                 drain_control: 'AbstractController' = FixedController.constant_controller()):
        self.t = 0
        self.flow_t = flow_t
        self.height = 0
        super().__init__(drain_control=drain_control, name='Source')

    def reset(self):
        self.t = 0
        super().reset()

    def update_height(self, dt):
        self.height = 0
        self.history['h'].append(self.height)
        self.history['Q'].append(self.get_drain_flow())
        self.history['output'].append(self.drain_control.output)
        self.t += dt

    def get_drain_flow(self) -> float:
        return self.flow_t(self.t)*self.get_control()

