from typing import Callable

from src.logic.fire_visitor import FireVisitor
from src.models.player import Player
from src.models.ship import CellState
from src.models.turn import Action, Turn
from src.models.turn_result import TurnResult


class TurnController:
    def __init__(self, player_one: Player, player_two: Player) -> None:
        self._players = {0: player_one, 1: player_two}
        self._current_player_index = 0
        self._who_made_turn: Player | None = None

        self._on_turn_made: Callable[[Player, TurnResult], None] | None = None

    @property
    def turn_made(self):
        return self._on_turn_made
    
    @turn_made.setter
    def turn_made(self, func):
        self._on_turn_made = func

    @property
    def who_makes_turn(self) -> Player:
        return self._players[self._current_player_index]
    
    @property
    def who_made_turn(self) -> Player:
        if self._who_made_turn is None:
            raise ValueError("No one has made turn yet")
        return self._who_made_turn

    def make_turn(self, point) -> TurnResult:
        current_player = self._players[self._current_player_index]
        opponent_player = self._players[1 - self._current_player_index]

        visitor = FireVisitor()
        result = opponent_player.board.accept(visitor, point)

        current_player.update_tracking_board(point, result)

        # if hit, current player gets another turn
        # if miss, switch player
        if result == CellState.MISS:
            self._current_player_index = 1 - self._current_player_index

        latest_turn = TurnResult(Turn(Action.SHOT, point),  opponent_player.board.get_ship_at(point), result)

        # TODO: make it through the tracking_board
        # provide feedback to the player about the result of their turn
        if self._on_turn_made:
            self._on_turn_made(current_player, latest_turn)

        self._who_made_turn = current_player

        return latest_turn

     