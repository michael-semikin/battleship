from abc import ABC, abstractmethod
import random

from logic.excecptions import InputError
from models.board import Point
from models.turn import Action, Turn


class InputProvider(ABC):
    @abstractmethod
    def get_input(self) -> Turn:
        pass

class ConsoleInputProvider(InputProvider):
    def get_input(self) -> Turn:
        try:
            user_input = input("\nYour turn: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return Turn(Action.QUIT)

        # Выход
        if user_input in ('q', 'quit', 'exit'):
            return Turn(Action.QUIT)
        
        if len(user_input) < 2:
                    raise InputError("Enter letter + number e.g. a5")

        column_part = user_input[0]
        row_part = user_input[1:]    

        try:
            row = int(row_part)
        except ValueError:
            raise InputError("Enter letter + number e.g. a5")

        column = ord(column_part) - ord('a')
        
        return Turn(Action.SHOT, Point(row, column))             
    
class RandomInputProvider(InputProvider):
    def get_input(self) -> Turn:
        random.seed()
        return Turn(Action.SHOT, Point(random.randrange(0, 9), random.randrange(0, 9)))     
