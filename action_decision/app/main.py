from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import asyncio

from .action_decider import ActionDecider

# Create FastAPI instance
app = FastAPI()
action_decider = ActionDecider()

# List of allowed origins (you can use '*' to allow all origins)
origins = [
    "http://localhost:3000",  # Allow your Next.js app
    # Add any other origins as needed
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Example route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI! This is the action decision server."}

@app.on_event("startup")
async def startup_event():
    pass

@app.get("/action_decision/get_game_state")
async def get_game_state():
    return await action_decider.get_game_state()

@app.get("/action_decision/get_decision")
async def get_decision():
    return await action_decider.decide()

@app.get("/action_decision/get_decision_tree")
async def get_decision_tree():
    return action_decider.get_decision_tree()

@app.get("/action_decision/stream_decision_tree")
async def stream_decision_tree():
    return StreamingResponse(action_decider.stream_decision_tree(), media_type="text/event-stream")

import time
def event_stream():
    count = 0
    while True:
        time.sleep(1)  # Simulate delay
        count += 1
        yield f"data: {count}\n\n"

@app.get("/stream_example")
async def get_events():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
