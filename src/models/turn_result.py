from dataclasses import dataclass

from src.models.common import CellState
from src.models.ship import Ship
from src.models.turn import Turn


@dataclass(frozen=True)
class TurnResult:
    turn: Turn
    ship: Ship | None
    result: CellState