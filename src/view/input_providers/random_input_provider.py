import random

from src.models.board import Board, Point
from src.models.turn import Action, Turn
from src.models.turn_result import TurnResult
from src.view.input_providers.input_provider import InputProvider


class RandomInputProvider(InputProvider):
    def get_input(self) -> Turn:
        random.seed()
        return Turn(Action.SHOT, Point(random.randrange(0, Board.BOX_SIZE - 1), random.randrange(0, Board.BOX_SIZE - 1)))
    
    def notify_result(self, turn_result: TurnResult):
        pass