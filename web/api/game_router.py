from fastapi import APIRouter, Request

from src.logic.game_engine import GameEngine
from src.view.input_providers.hunter_input_provider import HunterInputProvider
from src.view.models.transfer_objects import PlayerInfo, Point

game_router = APIRouter(prefix="/game", tags=["battleship game"])

@game_router.post('/start')
async def game_start(request: Request):
    game = GameEngine()
    game.init_game(None, HunterInputProvider())

    session = request.state.session.get_session()

    session["game"] = game

    player_info = PlayerInfo(name = game.player_one.name, 
                             board = tuple(game.player_one.board.matrix), 
                             trackingBoard = tuple(game.player_one.tracking_board.matrix))
    return player_info

@game_router.post("/make_turn")
async def make_turn(request: Request, point: Point):
    print(point.row, point.column)
    return "zzz"