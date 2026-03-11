import random

from src.models.board import Point
from src.models.common import BOARD_SIZE
from src.models.turn import Action, Turn
from src.models.turn_result import TurnResult
from src.view.input_providers.input_provider import InputProvider


class RandomInputProvider(InputProvider):
    def get_input(self) -> Turn:
        random.seed()
        return Turn(Action.SHOT, Point(random.randrange(0, BOARD_SIZE), random.randrange(0, BOARD_SIZE)))
    
    def notify_result(self, turn_result: TurnResult):
        pass