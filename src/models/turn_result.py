from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.models.ship import CellState, Ship
from src.models.turn import Turn

if TYPE_CHECKING:
    from src.models.player import Player


@dataclass(frozen=True)
class TurnResult:
    player: Player
    turn: Turn
    ship: Ship | None
    result: CellState