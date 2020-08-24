import numpy as np
import weakref

from ..controllers import AbstractController, FixedController


class Vessel:

    _instances = []

    def __init__(self, base_area: float = 250,
                 max_height: float = 1000000,
                 initial_height: float = 0,
                 source: 'Vessel' = None,
                 drain_pipe_area: float = 50,
                 drain_control: 'AbstractController' = FixedController.constant_controller(),
                 name=None):
        self.base_area = base_area
        self.max_height = max_height
        self.initial_height = initial_height
        self.height = initial_height
        self.drain_pipe_area = drain_pipe_area
        self.source = source
        self.drain = None
        self.drain_control = drain_control
        self.history = {'h': [], 'output': [], 'Q': []}
        self.last_q = 0
        self.net_q = 0

        if source:
            self.source.attach_drain(self)

        self._instances.append(weakref.ref(self))
        self.name = name

    def reset(self):
        self.height = self.initial_height
        self.drain_control.reset()
        self.history = {'h': [], 'output': [], 'Q': []}

    def get_pressure(self) -> float:
        return np.sqrt(self.height * 2 * 10)

    def get_control(self) -> float:
        return min(max(self.drain_control.output, 0), 1)

    def get_drain_flow(self) -> float:
        return self.drain_pipe_area * self.get_pressure() * self.get_control()

    def update_height(self, dt):
        """
        update updates the controller states and the height
        :param dt:
        """

        # update history
        self.history['h'].append(self.height)
        self.history['output'].append(self.drain_control.output)
        self.history['Q'].append(self.get_drain_flow())

        current_q = self.source.get_drain_flow() - self.get_drain_flow()
        # update state
        self.height += current_q/self.base_area * dt

        if self.height < 0:
            self.height = 0
        if self.height > self.max_height:
            self.height = self.max_height

        self.last_q = current_q

    def get_height(self, delay=0) -> float:
        if delay == 0:
            return self.height
        history_len = len(self.history['h'])
        if delay >= history_len:
            return self.initial_height
        return self.history['h'][history_len-1-delay]

    def update_control(self, dt: float):
        self.drain_control.update(dt)

    def attach_drain(self, drain: 'Vessel'):
        self.drain = drain

    @classmethod
    def reset_instances(cls):
        cls._instances = []

    @classmethod
    def get_instances(cls):
        dead = []
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.append(ref)
        for d in dead:
            cls._instances.remove(d)

