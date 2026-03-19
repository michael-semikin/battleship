import socketio
import secrets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastsession import FastSessionMiddleware, MemoryStore

from game_router import game_router
from socket_api import socket_server


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

game_store = MemoryStore()
app.add_middleware(
    FastSessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    store=game_store,
    session_cookie="game_session",
    max_age=3600,
    session_object="session"
)

app.include_router(game_router)

socket_app = socketio.ASGIApp(socket_server, app)

@app.get("/")
async def home_page():
    return "Hello there. Please use api methods"
