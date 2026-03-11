from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.models.common import Action

if TYPE_CHECKING:
    from src.models.board import Point

@dataclass(frozen=True)
class Turn:
    action: Action | None
    point: Point | None = None
