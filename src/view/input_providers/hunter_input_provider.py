import random
from collections import deque

from src.logic.turn_controller import TurnResult
from src.models.board import Board, Point
from src.models.common import BOARD_SIZE, Action
from src.models.turn import Turn
from src.view.input_providers.input_provider import InputProvider


class HunterInputProvider(InputProvider):
    def __init__(self):
        self._shots_fired: set[Point] = set()
        self._hunt_queue: deque[Point] = deque()
    
    def get_input(self) -> Turn:
        if self._hunt_queue:
            point = self._hunt_queue.popleft()
            if point not in self._shots_fired:
                self._shots_fired.add(point)
                return Turn(Action.SHOT, point)
        
        # if no point to fire then opponent won :)
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            point = Point(row, col)
            
            if point not in self._shots_fired:
                self._shots_fired.add(point)
                return Turn(Action.SHOT, point)
    
    def notify_result(self, turn_result: TurnResult):
        if turn_result.turn.point is None or turn_result.ship is None:
            return

        if turn_result.ship.is_alive:
            for neighbor in Board.get_neighbors(turn_result.turn.point):
                if neighbor not in self._shots_fired:
                    self._hunt_queue.append(neighbor)
        else:
            for neighbor in Board.get_surroundings(turn_result.turn.point):
                self._shots_fired.add(neighbor)            
            self._hunt_queue.clear()
    