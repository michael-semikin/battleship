"""this module is created for future use"""

import socketio


socket_server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', logger=True)

@socket_server.event
async def connect(sid, environ):
    print(f"Connected: {sid}")

@socket_server.event
async def disconnect(sid):
    print(f"🔌 Disconnected: {sid}")
