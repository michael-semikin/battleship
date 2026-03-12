from src.exceptions import InputError
from src.models.board import Point
from src.models.common import BOARD_SIZE
from src.models.turn import Action, Turn
from src.models.turn_result import TurnResult
from src.view.input_providers.input_provider import InputProvider


class ConsoleInputProvider(InputProvider):
    def get_input(self) -> Turn:
        try:
            user_input = input("\nYour turn: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return Turn(Action.QUIT)

        if user_input in ('q', 'quit', 'exit'):
            return Turn(Action.QUIT)
        
        if len(user_input) != 2:
            raise InputError("Enter letter + number e.g. a5")

        column_part = user_input[0]
        row_part = user_input[1:]

        if column_part < 'a' or column_part > 'j':
            raise InputError("Column must be a letter from a to j")

        if not row_part.isdigit() or int(row_part) < 0 or int(row_part) > BOARD_SIZE:
            raise InputError("Row must be a number from 0 to 9")

        row = int(row_part)

        column = ord(column_part) - ord('a')
        
        return Turn(Action.SHOT, Point(row, column))             
    
    def notify_result(self, turn_result: TurnResult):
        pass