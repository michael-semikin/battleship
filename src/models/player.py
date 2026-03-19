from functools import singledispatchmethod
from typing import Iterator

from src.models.board import Board
from src.models.common import CellState, Point


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self._main_board: Board = Board()
        self._tracking_board: Board = Board()

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        return self.name == other.name 

    @property
    def tracking_board(self) -> Board:
        return self._tracking_board
    
    @property
    def board(self) -> Board:
        return self._main_board
    
    def set_board(self, value: Board):
        self._main_board = value

    @singledispatchmethod
    def update_tracking_board(self, target, result: CellState | None = None):
        """ Generic entry point for updating the board. 
            Dispatches based on the type of 'target'.
        """        
        raise NotImplementedError(f"Unsupported target type: {type(target)}")
    
    @update_tracking_board.register
    def _(self, point: Point, result: CellState):
        """ updates the tracking board with the result of a shot
            Args:
                point (Point): the point that was shot at
                result (CellState): the result of the shot (HIT or MISS)
        """
 
        self._tracking_board[point] = result
    
    @update_tracking_board.register
    def _(self, board: Board, *args):
        """ updates the tracking board with the board passed
            Args:
                board (Point): the point that was shot at
        """

        self._tracking_board = board
        