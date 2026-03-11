from src.logic.fire import FireVisitor
from src.models.player import Player
from src.models.ship import CellState
from src.models.turn import Action, Turn
from src.models.turn_result import TurnResult


class TurnController:
    def __init__(self, player_one: Player, player_two: Player) -> None:
        self._players = {0: player_one, 1: player_two}
        self._current_player_index = 0
        self._who_made_turn: Player | None = None

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

        # provide feedback to the player about the result of their turn
        current_player.take_turn_result(latest_turn)

        self._who_made_turn = current_player

        return latest_turn

     