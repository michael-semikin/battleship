from enum import StrEnum, auto

from src.models.board import Point


class Action(StrEnum):
    QUIT = auto()
    SHOT = auto()

class Turn:
    def __init__(self, action: Action | None, point: Point | None = None) -> None:
        self.action: Action | None = action
        self.point: Point | None = point
