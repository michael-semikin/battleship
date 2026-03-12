from src.models.common import Point


class ShipAllocationError(Exception):
    """Raised when a ship cannot be allocated to the board."""

class AlreadyHitError(Exception):
    """Raised when a cell that has already been hit is targeted again."""
    def __init__(self, point: Point) -> None:
        super().__init__(f"Cell at {point} has already been targeted")
        self.point = point

class InputError(Exception):
    """Raised when a player provides invalid input"""        