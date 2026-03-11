import random
from collections import Counter
from collections.abc import Iterable
from typing import cast

from src.exceptions.already_hit_error import AlreadyHitError
from src.exceptions.input_error import InputError
from src.logic.logger import GameLogger
from src.logic.turn_controller import TurnController
from src.models.board import Board, Point
from src.models.common import BOARD_SIZE
from src.models.player import Player
from src.models.ship import Battleship, Cruiser, Destroyer, Scout, ShipType
from src.models.turn import Action
from src.view.input_providers.console_input_provider import \
    ConsoleInputProvider
from src.view.input_providers.hunter_input_provider import HunterInputProvider
from src.view.output_providers.view_provider import ViewProvider


class GameEngine:
    MAX_SHIP_PLACEMENT_ATTEMPTS = 100

    def __init__(self, view_provider: ViewProvider) -> None:
        self._player_one = Player("Player One", ConsoleInputProvider())
        self._player_two = Player("Player Two", HunterInputProvider())
        
        self._view_provider = view_provider
        self._logger = GameLogger()
        
    def init_game(self):
        """ initializes the game by creating two players and filling their boards with ships
        """

        self._player_one.set_board(self.fill_board())
        self._player_two.set_board(self.fill_board())

    def fill_board(self) -> Board:
        """ fills the board with ships in random positions and orientations
            Returns:
                Board: a board with ships placed on it
        """

        board = Board()

        # add ships to board
        fleet = ((Battleship, 1), (Cruiser, 2), (Destroyer, 3), (Scout, 4))

        for ship_type, count in fleet:
            for _ in range(count):             
                ship = ship_type()

                # find a random position and orientation for the ship
                for _ in range(GameEngine.MAX_SHIP_PLACEMENT_ATTEMPTS):  # try 100 times to find a valid position
                    ship.change_orientation(random.randint(0, len(ship.get_shapes()) - 1))

                    column = random.randint(0, BOARD_SIZE - 1)
                    row = random.randint(0, BOARD_SIZE - 1)
                    
                    if board.can_add_ship(ship, Point(row, column)):
                        board.add_ship(ship, Point(row, column))
                        break
                else:
                    raise RuntimeError(f"Failed to place ship {ship.name} after {GameEngine.MAX_SHIP_PLACEMENT_ATTEMPTS} attempts")
                
        return board

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
    
    def play(self):
        """ main loop
        """

        turn_controller = TurnController(self._player_one, self._player_two)

        is_over = False
        turn_count = 0
        
        while(True):
            # render view
            self._view_provider.clear_screen()
            self._view_provider.render(self._player_one)

            self._show_stats()
            self._view_provider.render_log(self._get_log())

            if (is_over):
                break

            # get user input for target cell
            try:
                player_input = turn_controller.who_makes_turn.get_input()
            except InputError as err:
                self._logger.log(f"{turn_controller.who_makes_turn.name} Invalid input: {err}")
                continue

            if player_input.action == Action.QUIT:
                self._logger.log(f"Game stopped by {turn_controller.who_makes_turn.name}")
                is_over = True
                continue

            try:
                result = turn_controller.make_turn(player_input.point)
            except AlreadyHitError as err:
                self._logger.log(f"{turn_controller.who_made_turn.name} Oops already hit at {err.point}")

            self._logger.log(f"{turn_count}| {turn_controller.who_made_turn.name} {result.result.name}", player_input)
            turn_count += 1                

            player_one_defeated = self._player_one.board.no_ships_remaining
            player_two_defeated = self._player_two.board.no_ships_remaining
            if player_one_defeated or player_two_defeated:
                # it is guaranteed that who_made_turn() will return a player, because the game can only end after a turn is made
                self._logger.log(f"Game won by {turn_controller.who_made_turn.name}")
                is_over = True                


    