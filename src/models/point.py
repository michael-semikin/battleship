from dataclasses import dataclass

from src.models.board import Board


@dataclass(frozen=True)
class Point:
    row: int
    column: int

    def __post_init__(self):
        if self.row < 0 or self.row >= Board.BOX_SIZE:
            raise ValueError(f"Row must be between 0 and {Board.BOX_SIZE - 1}")
        
        if self.column < 0 or self.column >= Board.BOX_SIZE:
            raise ValueError(f"Column must be between 0 and {Board.BOX_SIZE - 1}")

    def __iter__(self):
        return iter((self.row, self.column))
    
    def __str__(self) -> str:
        return f"{chr(ord('a') + self.column)}{self.row}"
    
    def __hash__(self) -> int:
        return hash((self.row, self.column))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.row == other.row and self.column == other.column