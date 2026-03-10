from abc import ABC, abstractmethod

from src.models.turn import Turn
from src.models.turn_result import TurnResult


class InputProvider(ABC):
    @abstractmethod
    def get_input(self) -> Turn:
        pass
 
    @abstractmethod
    def notify_result(self, turn_result: TurnResult):
        pass