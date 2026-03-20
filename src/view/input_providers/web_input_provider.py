from src.models.common import Point
from src.models.turn import Turn
from src.models.turn_result import TurnResult
from src.view.input_providers.input_provider import InputProvider


class WebInputProvider(InputProvider):
    def __init__(self) -> None:
        self._external_input: Point | None = None

    def get_input(self) -> Turn | None:
        return Turn(None, self._external_input)
    
    def notify_result(self, turn_result: TurnResult):
        pass

    def get_external_input(self, turn: Turn):
        self._external_input = turn.point