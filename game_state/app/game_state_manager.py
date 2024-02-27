from datetime import datetime
import asyncio

from shared.utils.image_utils import load_image, capture_screenshot

from .interactive_game_analyzer import InteractiveGameAnalyzer

UPDATE_INTERVAL = 3  # time in seconds between updates

class GameStateManager:
    def __init__(self):
        self.initialize_game_state()
        self.interactive_game_analyzer = InteractiveGameAnalyzer()
        self.update_game_state_periodically_flag = False
        print("GameStateManager initialized")
    
    def initialize_game_state(self):
        self.latest_game_state = {
            "success": False,
            "state": "No state available",
            "state_timestamp": None,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def update_game_state(self):
        success, state = await self.capture_and_process_game_state()
        self.latest_game_state['success'] = success
        self.latest_game_state['state'] = state
        self.latest_game_state['state_timestamp'] = datetime.utcnow().isoformat()
        self.latest_game_state['timestamp'] = datetime.utcnow().isoformat()
        return self.latest_game_state

    async def start_game_state_updates(self):
        self.update_game_state_periodically_flag = True
        asyncio.create_task(self.update_game_state_periodically())
    
    async def stop_game_state_updates(self):
        self.update_game_state_periodically_flag = False

    async def update_game_state_periodically(self):
        while self.update_game_state_periodically_flag:
            await self.update_game_state()
            await asyncio.sleep(UPDATE_INTERVAL)

    async def capture_and_process_game_state(self):
        screenshot = await self.capture_screenshot()
        success, state =  await self.process_screenshot(screenshot)
        return success, state

    async def capture_screenshot(self):
        print("Capturing screenshot...")
        return load_image('ffxiv1.jpg')  # Replace with capture_screenshot()

    async def process_screenshot(self, image):
        # Implementation to process the screenshot
        print("Processing screenshot...")
        return await self.interactive_game_analyzer.analyze_screenshot(image)

    def get_latest_game_state(self):
        if self.latest_game_state['state'] == "No state available":
            if self.check_model_server_status():
                self.latest_game_state['state'] = "Model server is up, but no state available"
                self.latest_game_state['state_timestamp'] = datetime.utcnow().isoformat()
        self.latest_game_state['timestamp'] = datetime.utcnow().isoformat()
        return self.latest_game_state
    
    def check_model_server_status(self):
        return self.interactive_game_analyzer.models_initialized