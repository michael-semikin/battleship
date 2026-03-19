from enum import IntEnum

from pydantic import BaseModel, Field

from src.models.common import ShipType


class ShipForm(IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1

class GameResult(IntEnum):
    LOST = 0
    WIN = 1

class Point(BaseModel):
    row: int
    column: int

class Ship(BaseModel):
    name: str
    type: ShipType
    form: ShipForm
    position: Point


class PlayerInfo(BaseModel):
    name: str
    main_board: tuple[tuple[int, ...], ...] = Field(alias="board")
    tracking_board: tuple[tuple[int, ...], ...] = Field(alias="trackingBoard")

class PlayerTurn(BaseModel):
    session_id: str
    name: str
    point: Point
