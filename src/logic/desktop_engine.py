from collections import Counter
from collections.abc import Iterable

from src.exceptions import AlreadyHitError, InputError
from src.logic.game_engine import GameEngine
from src.models.player import Player
from src.models.ship import ShipType
from src.models.turn import Action

from src.view.output_providers.view_provider import ViewProvider


class DesktopGameEngine(GameEngine):
    def __init__(self, view_provider: ViewProvider) -> None:
        super().__init__(view_provider)
 
    def _get_log(self)-> Iterable[str]:
        return tuple(f"{entry.date}: {entry.message} : {'shot at' if entry.turn else ' '} {entry.turn.point if entry.turn else ''}" 
                     for entry in self._logger.get_logs())
       
    def _get_ships_count(self, player: Player) -> Counter:
        return Counter((ship.type, ship.is_alive) for ship in player.board.ships)
    
    def _show_stats(self):
        player_one_ships = self._get_ships_count(self._player_one)
        player_two_ships = self._get_ships_count(self._player_two)
        ships_count = tuple(
                (player_one_ships[ship_type, True], player_two_ships[ship_type, False]) for ship_type in ShipType
                )
        self._view_provider.render_stats(ships_count)

    def _update_display(self):
            self._view_provider.clear_screen()
            self._view_provider.render(self._player_one)

            self._show_stats()
            self._view_provider.render_log(self._get_log())
    
    def _has_winner(self) -> bool:
        player_one_defeated = self._player_one.board.no_ships_remaining
        player_two_defeated = self._player_two.board.no_ships_remaining
        return player_one_defeated or player_two_defeated

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
            if self._has_winner():
                self._player_one.update_tracking_board(self._player_two.board)
                # it is guaranteed that who_made_turn() will return a player, because the game can only end after a turn is made
                self._logger.log(f"Game won by {self._turn_controller.who_made_turn.name}")
                is_over = True                
