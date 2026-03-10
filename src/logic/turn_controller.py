from src.logic.fire import FireVisitor
from src.models.player import Player
from src.models.ship import CellState
from src.models.turn import Action, Turn
from src.models.turn_result import TurnResult


class TurnController:
    def __init__(self, player_one: Player, player_two: Player) -> None:
        self._players = {0: player_one, 1: player_two}
        self._current_player_index = 0
        self._latest_turn: TurnResult | None = None

    @property
    def current_player(self) -> Player:
        return self._players[self._current_player_index]
    
    def get_latest_turn(self) -> TurnResult:
        if self._latest_turn is None:
            raise ValueError("No turns have been made yet")
        return self._latest_turn

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

        self._latest_turn = TurnResult(current_player, Turn(Action.SHOT, point),  opponent_player.board.get_ship_at(point), result)

        # provide feedback to the player about the result of their turn
        current_player.take_turn_result(self._latest_turn)

        return self._latest_turn

     