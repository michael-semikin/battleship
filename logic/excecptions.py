class ShipAllocationError(Exception):
    """Raised when a ship cannot be allocated to the board."""

class AlreadyHitError(Exception):
    """Raised when a cell that has already been hit is targeted again."""

class InputError(Exception):
    """Raised when a player provides invalid input"""