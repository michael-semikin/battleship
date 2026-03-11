from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from src.exceptions.ship_allocation_error import ShipAllocationError
from src.logic.acceptor import Acceptor
from src.models.common import BOARD_SIZE, CellState, Point
from src.models.ship import Ship

if TYPE_CHECKING:
    from src.logic.fire import Visitor

""" Board management for the Battleship game
    The board is represented as a 2D numpy array of integers, where each integer represents the state of the cell (empty, ship, hit, miss).
    The board also keeps track of the ships placed on it, and provides methods for adding ships, checking if a ship can be added, and getting the ship at a specific point.
    The board also implements the Visitor pattern to allow for firing at the board and applying damage to ships.
"""
class Board(Acceptor):
    def __init__(self) -> None:
        self._matrix_size = BOARD_SIZE
        self.matrix: NDArray[np.int_] = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self._ships: list[Ship] = []

    def __getitem__(self, point: Point) -> CellState:
        return CellState(self.matrix[*point])

    def __setitem__(self, point: Point, value: CellState):
        self.matrix[*point] = value

    def add_ship(self, ship: Ship, position: Point):
        if not self.can_add_ship(ship, position):
            raise ShipAllocationError(
                f"Cannot add ship {ship.name} at position {position}"
            )

        for row_idx in range(ship.shape.shape[0]):
            for col_idx in range(ship.shape.shape[1]):
                self.matrix[position.row + row_idx, position.column + col_idx] = (
                    ship.shape[row_idx, col_idx]
                )

        self._ships.append(ship)
        ship.position = position

    def can_add_ship(self, ship: Ship, position: Point) -> bool:
        height, width = ship.shape.shape

        if (
            position.row + height > self._matrix_size
            or position.column + width > self._matrix_size
        ):
            return False

        start_row = max(position.row - 1, 0)
        end_row = min(position.row + height + 1, self._matrix_size)
        start_col = max(position.column - 1, 0)
        end_col = min(position.column + width + 1, self._matrix_size)

        target_area = self.matrix[start_row:end_row, start_col:end_col]

        if np.any(target_area == CellState.SHIP):
            return False

        return True

    """ Returns the ship at the given point, or None if there is no ship at that point.
        Args:
            point (Point): the point to check for a ship
        Returns:
            Ship | None: the ship at the given point, or None if there is no ship at that point"""
    def get_ship_at(self, point: Point) -> Ship | None:
        for ship in self._ships:
            if ship.position is None:
                raise ShipAllocationError(f"Ship {ship.name} has no position allocated")

            ship_row, ship_column = ship.position
            ship_height, ship_width = ship.shape.shape

            if (ship_row <= point.row < ship_row + ship_height) and (
                ship_column <= point.column < ship_column + ship_width
            ):
                return ship

        return None

    @property
    def ships(self) -> list[Ship]:
        return self._ships

    @property
    def no_ships_remaining(self) -> bool:
        return all(not ship.is_alive for ship in self._ships)

    """ Accepts a visitor to perform an action on the board, such as firing at a specific point.
        Args:
            visitor (Visitor): the visitor to accept
            point (Point): the point to target with the visitor's action"""

    def accept(self, visitor: Visitor, point: Point) -> CellState:
        return visitor.visit_board(self, point)

    @staticmethod
    def get_neighbors(point: Point) -> set[Point]:
        neighbors: set[Point] = set()
        # horizontal neighbors
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            row, col = point.row + dr, point.column + dc
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                neighbors.add(Point(row, col))
        return neighbors

    @staticmethod
    def get_surroundings(point: Point) -> set[Point]:
        surroundings: set[Point] = Board.get_neighbors(point)

        # 2. Добавляем только диагонали
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in diagonals:
            row, col = point.row + dr, point.column + dc
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                surroundings.add(Point(row, col))

        return surroundings
