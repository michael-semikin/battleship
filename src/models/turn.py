from __future__ import annotations

from typing import TYPE_CHECKING

from enum import StrEnum, auto

if TYPE_CHECKING:
    from src.models.board import Point


class Action(StrEnum):
    QUIT = auto()
    SHOT = auto()

class Turn:
    def __init__(self, action: Action | None, point: Point | None = None) -> None:
        self.action: Action | None = action
        self.point: Point | None = point
