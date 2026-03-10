from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import IntEnum, StrEnum, auto
import textwrap
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from src.logic.acceptor import Acceptor

if TYPE_CHECKING:
    from src.models.board import Point
    from src.logic.fire import Visitor


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

    @property
    def description(self): 
        return self.capitalize()

class Ship(Acceptor, metaclass=ABCMeta):
    def __init__(self, type: ShipType, name: str, shape: NDArray[np.int_]) -> None:
        self.type: ShipType = type
        self.name: str = name
        self.shape: NDArray[np.int_] = shape
        
        self.position: Point| None = None
        self.hit_points: int = 0

    @abstractmethod
    def get_shapes(self)-> tuple[NDArray[np.int_], ...]:
        raise NotImplementedError
    
    def change_orientation(self, orientation: int):
        if self.shape is None:
            raise ValueError("Ship shape is not set")
        
        if orientation < 0 or orientation >= len(self.get_shapes()):
            raise ValueError(f"Invalid orientation {orientation} for ship {self.name}")
        
        shapes = self.get_shapes()
        self.shape = shapes[orientation]

    @property
    def is_alive(self) -> bool:
        return self.hit_points > 0
    
    def apply_damage(self):
        if self.hit_points <= 0:
            raise ValueError(f"Ship {self.name} is already destroyed")
        
        self.hit_points -= 1

    def accept(self, visitor: Visitor, point: Point | None = None): 
        visitor.visit_ship(self)

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
        self.hit_points = 1

    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape,)
    
class Destroyer(Ship):
    def __init__(self) -> None:
        super().__init__(ShipType.DESTROYER, "Destroyer", np.array([[CellState.SHIP] * 2]))
        self.hit_points = 2
    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape, self.shape.T)

class Cruiser(Ship):
    def __init__(self) -> None:
        super().__init__(ShipType.CRUISER, "Cruiser", np.array([[CellState.SHIP] * 3]))
        self.hit_points = 3
    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape, self.shape.T)

class Battleship(Ship):
    def __init__(self) -> None:
        super().__init__(ShipType.BATTLESHIP, "Battleship", np.array([[CellState.SHIP] * 4]))
        self.hit_points = 4
    def get_shapes(self) -> tuple[NDArray[np.int_], ...]:
        return (self.shape, self.shape.T)