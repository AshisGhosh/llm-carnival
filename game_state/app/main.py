from fastapi import FastAPI
from .game_state_manager import GameStateManager
import asyncio

# Create FastAPI instance
app = FastAPI()
game_state_manager = GameStateManager()

# Example route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(game_state_manager.update_game_state_periodically())

@app.get("/game_state/get_game_state")
async def get_current_game_state():
    return game_state_manager.get_latest_game_state()