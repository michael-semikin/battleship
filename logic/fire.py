from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from logic.excecptions import AlreadyHitError
from models.ship import CellState

if TYPE_CHECKING:
    from models.board import Board
    from models.board import Point
    from models.ship import Ship

class Visitor(metaclass=ABCMeta):

    @abstractmethod
    def visit_board(self, board: Board, point: Point) -> CellState:
        pass

    @abstractmethod
    def visit_ship(self, ship: Ship):
        pass

class FireVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()

    def visit_board(self, board: Board, point: Point) -> CellState:
        hit_cell = board.matrix[*point]
        
        if hit_cell in {CellState.HIT, CellState.MISS}:
            raise AlreadyHitError(f"Cell at {point} has already been targeted")

        if hit_cell == CellState.SHIP:
            target = board.get_ship_at(point)
            if target:
                target.accept(self)
                board.matrix[*point] = CellState.HIT
        elif hit_cell == CellState.EMPTY:
            board.matrix[*point] = CellState.MISS

        return board[point]

    def visit_ship(self, ship: Ship):
        ship.apply_damage()
