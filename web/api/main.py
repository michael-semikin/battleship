import socketio
import secrets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastsession import FastSessionMiddleware, MemoryStore

from game_router import game_router
from socket_api import socket_server

class ConsoleLogger:
    def info(self, str):
        print(f"[INFO]{str}")
        pass

    def debug(self, str):
        print(f"[DEBUG]{str}")
        pass

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,  
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(
    FastSessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    secure=False,
    store=MemoryStore(),
    session_cookie="game_session",
    same_site="lax",
    logger = ConsoleLogger()
)

app.include_router(game_router)

socket_app = socketio.ASGIApp(socket_server, app)

@app.get("/")
async def home_page():
    return "Hello there. Please use api methods"
