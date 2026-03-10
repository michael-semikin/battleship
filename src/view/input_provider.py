from abc import ABC, abstractmethod
import random

from src.models.board import Point
from src.models.turn import Action, Turn


class InputProvider(ABC):
    @abstractmethod
    def get_input(self) -> Turn:
        pass
 
class RandomInputProvider(InputProvider):
    def get_input(self) -> Turn:
        random.seed()
        return Turn(Action.SHOT, Point(random.randrange(0, 9), random.randrange(0, 9)))    