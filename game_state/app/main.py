from fastapi import FastAPI
from .game_state_manager import GameStateManager
import asyncio

from shared.utils.client_utils.model_server import check_model_server_status

# Create FastAPI instance
app = FastAPI()
game_state_manager = GameStateManager()

# Example route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI! This is the game state server."}

@app.on_event("startup")
async def startup_event():
    pass

@app.get("/game_state/update_game_state")
async def update_game_state():
    return await game_state_manager.update_game_state()

@app.get("/game_state/start_game_state_updates")
async def start_game_state_updates():
    await game_state_manager.start_game_state_updates()
    return {"message": "Game state updates started."}

@app.get("/game_state/stop_game_state_updates")
async def stop_game_state_updates():
    await game_state_manager.stop_game_state_updates()
    return {"message": "Game state updates stopped."}

@app.get("/game_state/get_game_state")
async def get_current_game_state():
    return game_state_manager.get_latest_game_state()

@app.get("/game_state/check_model_server_status")
async def check_model_server():
    return {"status": await check_model_server_status()}

@app.get("/game_state/analyzer/analyze_screenshot")
async def analyze_screenshot():
    return await game_state_manager.capture_and_process_game_state()

@app.get("/game_state/analyzer/get_vqa_response")
async def get_vqa_response(question:str):
    image = await game_state_manager.capture_screenshot()
    return await game_state_manager.interactive_game_analyzer.get_vqa_response(question, image)