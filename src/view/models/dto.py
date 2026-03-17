from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel

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
    session_id: str
    name: str
    main_board: tuple[tuple[int]]
    tracking_board: tuple[tuple[int]]

class PlayerTurn(BaseModel):
    session_id: str
    name: str
    point: Point
