from enum import IntEnum, StrEnum, auto


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