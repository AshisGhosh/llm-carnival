from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import io
import asyncio
from PIL import Image

from .game_state_manager import GameStateManager

from shared.utils.client_utils.model_server import check_model_server_status

# Create FastAPI instance
app = FastAPI()
game_state_manager = GameStateManager()

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

@app.get("/game_state/stream_analyzer_status")
async def stream_analyzer_status():
    return StreamingResponse(game_state_manager.interactive_game_analyzer.stream_status(), media_type="text/event-stream")

@app.post("/game_state/update_image")
async def update_image(image: UploadFile = File(...)):
     # Read the image file in memory
    image_data = await image.read()
    
    # Convert the image data to a PIL Image
    image = Image.open(io.BytesIO(image_data))
    
    return game_state_manager.update_image(image)

@app.get("/game_state/get_image")
async def get_image():
    image = game_state_manager.get_image()
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')  # Adjust format as necessary
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/jpeg")