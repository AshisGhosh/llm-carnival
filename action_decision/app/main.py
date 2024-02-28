from fastapi import FastAPI
import asyncio

from .action_decider import ActionDecider

# Create FastAPI instance
app = FastAPI()
action_decider = ActionDecider()

# Example route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI! This is the action decision server."}

@app.on_event("startup")
async def startup_event():
    pass

@app.get("/action_decision/get_game_state")
async def get_game_state():
    return action_decider.get_game_state()

@app.get("/action_decision/get_decision")
async def get_decision():
    return await action_decider.decide()