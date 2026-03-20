from fastapi import APIRouter, Request

from src.logic.web_engine import WebGameEngine
from src.models.common import Point
from src.models.turn import Turn
from src.view.input_providers.hunter_input_provider import HunterInputProvider
from src.view.input_providers.web_input_provider import WebInputProvider
from src.view.models.transfer_objects import PlayerInfo, Point as PointDto


"""The primary objective of this module is to illustrate web backend connectivity while also featuring the Vue web interface.
"""
game_router = APIRouter(prefix="/game", tags=["battleship game"])

GAME_SESSION_KEY = "game"
INPUT_SESSION_KEY = "input"

@game_router.post('/start')
async def game_start(request: Request):
    game = WebGameEngine()
    input_provider = WebInputProvider()
    game.init_game(input_provider, HunterInputProvider())

    session = request.state.session
    mgr = session.get_session()

    if GAME_SESSION_KEY not in mgr:
        mgr[GAME_SESSION_KEY] = game
        mgr[INPUT_SESSION_KEY] = input_provider

    player_info = PlayerInfo(name = game.player_one.name, 
                             board = tuple(game.player_one.board.matrix), 
                             trackingBoard = tuple(game.player_one.tracking_board.matrix))
    
    return player_info

@game_router.post("/make_turn")
async def make_turn(request: Request, point: PointDto):

    session = request.state.session.get_session()
    game: WebGameEngine = session.get(GAME_SESSION_KEY)
    input: WebInputProvider = session.get(INPUT_SESSION_KEY)

    if not game or not input:
        print("no game objects are in session")
        return
    
    user_input = Point(point.row, point.column)
    input.get_external_input(Turn(None, point=user_input))
    game.play()
        


@game_router.post('/update_board')
async def update_board(request: Request):
    session = request.state.session.get_session()
    game: WebGameEngine = session.get(GAME_SESSION_KEY)

    if not game:
        print("no game objects are in session")
        return    
    player_info = PlayerInfo(name = game.player_one.name, 
                             board = tuple(game.player_one.board.matrix), 
                             trackingBoard = tuple(game.player_one.tracking_board.matrix))
    
    return player_info
