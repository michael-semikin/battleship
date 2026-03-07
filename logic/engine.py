# create board

import random

from models.board import Board, Point
from models.ship import Battleship, Cruiser, Destroyer, Scout, Ship, ShipType

class GameEngine:
    MAX_SHIP_PLACEMENT_ATTEMPTS = 100

    def __init__(self):
        pass

    def init_game(self):
        board = Board()

        # add ships to board
        fleet = ((Battleship, 1), (Cruiser, 2), (Destroyer, 3), (Scout, 4))

        for ship_type, count in fleet:
            for _ in range(count):             
                ship = ship_type()

                # find a random position and orientation for the ship
                for _ in range(GameEngine.MAX_SHIP_PLACEMENT_ATTEMPTS):  # try 100 times to find a valid position
                    x = random.randint(0, board.BOARD_HEIGHT - 1)
                    y = random.randint(0, board.BOARD_WIDTH - 1)
                    
                    if board.can_add_ship(ship, Point(x, y)):
                        board.add_ship(ship, Point(x, y))
                        ship.change_orientation(random.randint(0, len(ship.get_shapes()) - 1))
                        break


        print(board.matrix)
        print(board.ships)

# implement shooting logic