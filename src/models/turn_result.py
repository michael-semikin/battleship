from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.models.common import CellState
from src.models.ship import Ship
from src.models.turn import Turn

if TYPE_CHECKING:
    from src.models.player import Player


@dataclass(frozen=True)
class TurnResult:
    turn: Turn
    ship: Ship | None
    result: CellState