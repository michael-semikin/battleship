from logic.fire import FireVisitor
from models.players import Player
from models.ship import CellState


class TurnController:
    def __init__(self, player_one: Player, player_two: Player) -> None:
        self.players = {0: player_one, 1: player_two}
        self.current_player_index = 0

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def make_turn(self, point):
        current_player = self.players[self.current_player_index]
        opponent_player = self.players[1 - self.current_player_index]

        visitor = FireVisitor()
        result = opponent_player.board.accept(visitor, point)

        current_player.update_tracking_board(point, result)

        # if hit, current player gets another turn
        # if miss, switch player
        if result == CellState.MISS:
            self.current_player_index = 1 - self.current_player_index


     