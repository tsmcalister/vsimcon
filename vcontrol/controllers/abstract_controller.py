from typing import Callable
from abc import ABC, abstractmethod


class AbstractController(ABC):
    @property
    @abstractmethod
    def output(self) -> float:
        ...

    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def update(self, dt: float):
        ...
