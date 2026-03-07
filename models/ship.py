from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import IntEnum, StrEnum, auto
import textwrap
import textwrap
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from models.board import Point


class CellState(IntEnum):
    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3

class ShipType(StrEnum):
    SCOUT = auto()
    DESTROYER = auto()
    CRUISER = auto()
    BATTLESHIP = auto()

class Ship(metaclass=ABCMeta):
    def __init__(self, type: ShipType, name: str, shape: NDArray[np.int_]) -> None:
        self.type: ShipType = type
        self.name: str = name
        self.shape: NDArray[np.int_] = shape
        self.position: Point| None = None

    @abstractmethod
    def get_shapes(self)-> tuple[NDArray[np.int_], ...]:
        pass

    def __repr__(self) -> str:
        return textwrap.dedent(f"""
            {self.name}:
            Type: {self.type}
            Shape: {self.shape}
            Position: {self.position}
        """)

class Scout(Ship):
    def __init__(self) -> None:
        super().__init__(ShipType.SCOUT, "Scout", np.array([[CellState.SHIP]]))

    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape,)

class Destroyer(Ship):
    def __init__(self) -> None:
        super().__init__(ShipType.DESTROYER, "Destroyer", np.array([[CellState.SHIP] * 2]))
        
    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape, self.shape.T)

class Cruiser(Ship):
    def __init__(self) -> None:
        super().__init__(ShipType.CRUISER, "Cruiser", np.array([[CellState.SHIP] * 3]))

    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape, self.shape.T)

class Battleship(Ship):
    def __init__(self) -> None:
        super().__init__(ShipType.BATTLESHIP, "Battleship", np.array([[CellState.SHIP] * 4]))
        
    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape, self.shape.T)