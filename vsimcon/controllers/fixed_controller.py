from .abstract_controller import AbstractController
from typing import Callable


class FixedController(AbstractController):
    def __init__(self, phi_t: Callable[[float], float]):
        self.t = 0
        self.phi_t = phi_t

    @property
    def output(self) -> float:
        return self.phi_t(self.t)

    def update(self, dt: float):
        self.t += dt

    def reset(self):
        self.t = 0

    @classmethod
    def constant_controller(cls, output: float = 1) -> 'FixedController':
        """
        Initialises a constant controller that doesn't change its output
        :param output: the constant output of the controller
        :return: a FixedController instance
        """
        return cls(lambda x: output)


