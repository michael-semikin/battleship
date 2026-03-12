from functools import singledispatchmethod

from src.models.board import Board
from src.models.common import CellState, Point
from src.models.turn import Turn
from src.models.turn_result import TurnResult
from src.view.input_providers.input_provider import InputProvider


class Player:
    def __init__(self, name: str, input_provider: InputProvider):
        self.name: str = name
        self._main_board: Board = Board()
        self._tracking_board: Board = Board()
        self._input_provider = input_provider

    @property
    def tracking_board(self) -> Board:
        return self._tracking_board
    
    @property
    def board(self) -> Board:
        return self._main_board
    
    def get_input(self) -> Turn:
        return self._input_provider.get_input()
    
    def take_turn_result(self, turn_result: TurnResult):
        self._input_provider.notify_result(turn_result)
    
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