import random

from models.board import Board, Point
from models.players import Player
from models.ship import Battleship, CellState, Cruiser, Destroyer, Scout
from view.view_provider import ViewProvider

class GameEngine:
    MAX_SHIP_PLACEMENT_ATTEMPTS = 100

    def __init__(self, view_provider: ViewProvider) -> None:
        self.players = (Player("Player One"), Player("Player Two"))
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

        # TODO: display all the users boards
        self.players[0].update_tracking_board(Point(1,1), CellState.MISS)
        self.players[0].update_tracking_board(Point(1,3), CellState.HIT)
        self.view_provider.render(self.players[0])

        #print(self.players[0].board.matrix)


        while(False):
            # ViewProvider.invalidate views
            # TODO: get user input for target cell
            #   validate input
            #   convert to Point

            # TODO: Implement TurnController
            #   player 1 turn
            #   inform player 2
            #   if hit
            #     mark tracking board 
            #     loop

            pass