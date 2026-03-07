from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from logic.excecptions import ShipAllocationError
from models.ship import CellState

if TYPE_CHECKING:
    from models.ship import Ship


@dataclass(frozen=True)
class Point:
    row: int
    column: int

    def __post_init__(self):
        if self.row < 0 or self.row >= Board.BOARD_HEIGHT:
            raise ValueError(f"Row must be between 0 and {Board.BOARD_HEIGHT - 1}")
        if self.column < 0 or self.column >= Board.BOARD_WIDTH:
            raise ValueError(f"Column must be between 0 and {Board.BOARD_WIDTH - 1}")

    def __iter__(self):
        return iter((self.row, self.column))

class Board:
    BOARD_HEIGHT = 10
    BOARD_WIDTH = 10    

    def __init__(self) -> None:
        self.matrix: NDArray[np.int_] = np.zeros((10, 10), dtype=int)
        self.ships: list[Ship] = []

    def add_ship(self, ship: Ship, position: Point):
        if not self.can_add_ship(ship, position):
            raise ShipAllocationError(f"Cannot add ship {ship.name} at position {position}")
        
        for row_idx in range(ship.shape.shape[0]):
            for col_idx in range(ship.shape.shape[1]):
                self.matrix[position.row + row_idx, position.column + col_idx] = ship.shape[row_idx, col_idx]

        self.ships.append(ship)
        ship.position = position

    def can_add_ship(self, ship: Ship, position: Point) -> bool:
        height, width = ship.shape.shape

        if position.row + height > Board.BOARD_HEIGHT or position.column + width > Board.BOARD_WIDTH:
            return False
        
        start_row = max(position.row - 1, 0)
        end_row = min(position.row + height + 1, Board.BOARD_HEIGHT)
        start_col = max(position.column - 1, 0)
        end_col = min(position.column + width + 1, Board.BOARD_WIDTH)

        target_area = self.matrix[start_row:end_row, start_col:end_col]

        if np.any(target_area == CellState.SHIP):
            return False
        
        return True

        