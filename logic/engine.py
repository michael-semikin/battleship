import random

from logic.turn_controller import TurnController
from models.board import Board, Point
from models.players import Player
from models.ship import Battleship, Cruiser, Destroyer, Scout

from models.turn import Action
from view.input_provider import ConsoleInputProvider, RandomInputProvider
from view.view_provider import ViewProvider

class GameEngine:
    MAX_SHIP_PLACEMENT_ATTEMPTS = 100

    def __init__(self, view_provider: ViewProvider) -> None:
        self.players = (
            Player("Player One", ConsoleInputProvider()), 
            Player("Player Two", RandomInputProvider())
            )
        self.view_provider = view_provider
        
    def init_game(self):
        """ initializes the game by creating two players and filling their boards with ships
        """

        for idx in range(len(self.players)):
            self.players[idx].set_board(self.fill_board())

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

                    column = random.randint(0, board.BOX_SIZE - 1)
                    row = random.randint(0, board.BOX_SIZE - 1)
                    
                    if board.can_add_ship(ship, Point(row, column)):
                        board.add_ship(ship, Point(row, column))
                        break
                else:
                    raise RuntimeError(f"Failed to place ship {ship.name} after {GameEngine.MAX_SHIP_PLACEMENT_ATTEMPTS} attempts")
                
        return board
        
    def play(self):
        """ main loop
        """

        turn_controller = TurnController(*self.players)
        print(self.players[1].board.matrix)

        is_over = False
        while(not is_over):
            # ViewProvider.invalidate views
            self.view_provider.invalidate()
            self.view_provider.render(self.players[0])

            # get user input for target cell
            player_input = turn_controller.current_player.get_input()
            if player_input.action == Action.QUIT:
                is_over = True

            # Implement TurnController
            turn_controller.make_turn(player_input.point)

            player_one_defeated = self.players[0].board.no_ships_remaining
            player_two_defeated = self.players[1].board.no_ships_remaining
            is_over = player_one_defeated or player_two_defeated            

            