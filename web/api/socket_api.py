"""this module is created for future use"""

import socketio


socket_server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=['http://localhost:5173'], logger=True)

@socket_server.event
async def connect(sid, environ):
    print(f"Socket connected: {sid}")

@socket_server.event
async def disconnect(sid):
    print(f"🔌 Socket disconnected: {sid}")
