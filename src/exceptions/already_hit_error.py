from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.board import Point


class AlreadyHitError(Exception):
    """Raised when a cell that has already been hit is targeted again."""
    def __init__(self, point: Point) -> None:
        super().__init__(f"Cell at {point} has already been targeted")
        self.point = point