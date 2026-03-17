from fastapi.responses import RedirectResponse

from web.api.routers import game_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(game_router)

@app.get("/")
def home_page():
    return RedirectResponse(url="/game")