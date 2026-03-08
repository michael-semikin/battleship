# Player management for the Battleship game 
from models.board import Board
from models.ship import CellState


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self._main_board: Board = Board()
        self._tracking_board: Board = Board()

    @property
    def tracking_board(self) -> Board:
        return self._tracking_board
    
    @property
    def board(self) -> Board:
        return self._main_board
    
    def set_board(self, value: Board):
        self._main_board = value

    def update_tracking_board(self, point, result: CellState):
        """ updates the tracking board with the result of a shot
            Args:
                point (Point): the point that was shot at
                result (CellState): the result of the shot (HIT or MISS)
        """
 
        self._tracking_board.matrix[point.row, point.column] = result
     