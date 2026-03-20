from src.exceptions.base import AlreadyHitError, InputError
from src.logic.game_engine import GameEngine


class WebGameEngine(GameEngine):
    def __init__(self) -> None:
        super().__init__()
        self._turn_controller.turn_made = lambda player, latest_turn: self._player_inputs[player].notify_result(latest_turn)

    def play(self):
        while not self.has_winner():
            try:
                player_input = self._player_inputs[self._turn_controller.who_makes_turn].get_input()
            except InputError as err:
                self._logger.log(f"{self._turn_controller.who_makes_turn.name} Invalid input: {err}")
                break

            try:
                result = self._turn_controller.make_turn(player_input.point)

                self._logger.log(f"{self._turn_controller.who_made_turn.name} {result.result.name}", player_input)

                # if a real player (web ui) must make a turn or game is over we will break the loop
                if self.has_winner() or self._turn_controller.who_makes_turn is self._player_one:
                    # required to check if we have a winner and write the log message down
                    break

                print("we're in game loop")
            except AlreadyHitError as err:
                self._logger.log(f"{self._turn_controller.who_made_turn.name} Oops already hit at {err.point}")
                break

        if self.has_winner():
            self._player_one.update_tracking_board(self._player_two.board)
            # it is guaranteed that who_made_turn() will return a player, because the game can only end after a turn is made
            self._logger.log(f"Game won by {self._turn_controller.who_made_turn.name}")
