import random

from src.logic.logger import GameLogger
from src.logic.turn_controller import TurnController
from src.models.board import Board
from src.models.common import BOARD_SIZE, Point
from src.models.player import Player
from src.models.ship import Battleship, Cruiser, Destroyer, Scout
from src.view.input_providers.input_provider import InputProvider

class GameEngine:
    MAX_SHIP_PLACEMENT_ATTEMPTS = 100
    
    def __init__(self) -> None:
        self._player_one = Player("Player One")
        self._player_two = Player("Player Two")

        self._player_inputs: dict[Player, InputProvider] = { }
        
        self._turn_controller = TurnController(self._player_one, self._player_two)
        self._logger = GameLogger()

    @property
    def player_one(self) -> Player:
        return self._player_one
    
    @property
    def player_two(self) -> Player:
        return self._player_two
    
    @property
    def turn_controller(self) -> TurnController:
        return self._turn_controller        

    def init_game(self, input_provider_one: InputProvider | None, input_provider_two: InputProvider | None):
        """ initializes the game by creating two players and filling their boards with ships
        """

        self._player_one.set_board(self._fill_board())
        self._player_two.set_board(self._fill_board())

        if not self._player_inputs.get(self._player_one) and input_provider_one is not None:
            self._player_inputs[self._player_one] = input_provider_one
        if not self._player_inputs.get(self._player_two) and input_provider_two is not None :
            self._player_inputs[self._player_two] = input_provider_two        
        
    def _fill_board(self) -> Board:
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
                for _ in range(self.MAX_SHIP_PLACEMENT_ATTEMPTS):  # try 100 times to find a valid position
                    ship.change_orientation(random.randint(0, len(ship.get_shapes()) - 1))

                    column = random.randint(0, BOARD_SIZE - 1)
                    row = random.randint(0, BOARD_SIZE - 1)
                    
                    if board.can_add_ship(ship, Point(row, column)):
                        board.add_ship(ship, Point(row, column))
                        break
                else:
                    raise RuntimeError(f"Failed to place ship {ship.name} after {self.MAX_SHIP_PLACEMENT_ATTEMPTS} attempts")
                
        return board        