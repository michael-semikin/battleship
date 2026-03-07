
from models.board import Board, Point
from models.ship import Destroyer


def main():
    board = Board()

    print(board.add_ship(Destroyer(), Point(1, 0)))
    
    print(board.add_ship(Destroyer(), Point(1, 3)))

    print(board.matrix)
    print(repr(board.ships[0]))


if __name__ == "__main__":
    main()
