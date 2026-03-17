from fastapi import APIRouter

from src.view.models.dto import PlayerInfo


router = APIRouter(prefix="/game", tags=["battleship game"])

@router.get("game", summary="get player info")
def get_player_info() -> PlayerInfo:
    info = PlayerInfo()
    return info