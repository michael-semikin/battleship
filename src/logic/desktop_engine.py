from src.exceptions import AlreadyHitError, InputError
from src.logic.game_engine import GameEngine
from src.models.turn import Action

from src.view.output_providers.view_provider import ViewProvider


class DesktopGameEngine(GameEngine):
    def __init__(self, view_provider: ViewProvider) -> None:
        super().__init__()
        self._view_provider = view_provider
    
    def display_stats(self):
        self._view_provider.render_stats(self.calculate_stats())     

    def _update_display(self):
            self._view_provider.clear_screen()
            self._view_provider.render(self._player_one)

            self.display_stats()
            self._view_provider.render_log(self.get_log())

    def play(self):
        """ main loop
        """

        is_over = False
        turn_count = 0

        self._turn_controller.turn_made = lambda player, latest_turn: self._player_inputs[player].notify_result(latest_turn)
        
        while True:
            # render view
            self._update_display()

            if is_over:
                break

            # main action
            try:
                player_input = self._player_inputs[self._turn_controller.who_makes_turn].get_input()
            except InputError as err:
                self._logger.log(f"{self._turn_controller.who_makes_turn.name} Invalid input: {err}")
                continue

            if player_input.action == Action.QUIT:
                self._logger.log(f"Game stopped by {self._turn_controller.who_makes_turn.name}")
                is_over = True
                continue

            try:
                result = self._turn_controller.make_turn(player_input.point)
            except AlreadyHitError as err:
                self._logger.log(f"{self._turn_controller.who_made_turn.name} Oops already hit at {err.point}")
                continue

            self._logger.log(f"{turn_count}| {self._turn_controller.who_made_turn.name} {result.result.name}", player_input)
            turn_count += 1                

            # win/defeat condition
            if self.has_winner():
                self._player_one.update_tracking_board(self._player_two.board)
                # it is guaranteed that who_made_turn() will return a player, because the game can only end after a turn is made
                self._logger.log(f"Game won by {self._turn_controller.who_made_turn.name}")
                is_over = True                
