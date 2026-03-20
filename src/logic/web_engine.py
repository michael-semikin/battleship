from src.exceptions.base import AlreadyHitError, InputError
from src.logic.game_engine import GameEngine


class WebGameEngine(GameEngine):
    def __init__(self) -> None:
        super().__init__()
        self._turn_controller.turn_made = lambda player, latest_turn: self._player_inputs[player].notify_result(latest_turn)

    def play(self):
        while True:
            try:
                player_input = self._player_inputs[self._turn_controller.who_makes_turn].get_input()
            except InputError as err:
                self._logger.log(f"{self._turn_controller.who_makes_turn.name} Invalid input: {err}")
                continue

            try:
                result = self._turn_controller.make_turn(player_input.point)
                if self._turn_controller.who_makes_turn is self._player_one:
                    break                
            except AlreadyHitError as err:
                self._logger.log(f"{self._turn_controller.who_made_turn.name} Oops already hit at {err.point}")
                continue
