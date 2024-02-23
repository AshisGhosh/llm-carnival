from datetime import datetime
import asyncio

from shared.utils.image_utils import load_image, capture_screenshot

from .interactive_game_analyzer import InteractiveGameAnalyzer

UPDATE_INTERVAL = 3  # time in seconds between updates

class GameStateManager:
    def __init__(self):
        self.latest_game_state = {}
        self.interactive_game_analyzer = InteractiveGameAnalyzer()
        print("GameStateManager initialized")
    
    async def update_game_state_periodically(self):
        while True:
            success, state = await self.capture_and_process_game_state()
            self.latest_game_state['success'] = success
            self.latest_game_state['state'] = state
            self.latest_game_state['timestamp'] = datetime.utcnow().isoformat()
            await asyncio.sleep(UPDATE_INTERVAL)

    async def capture_and_process_game_state(self):
        screenshot = await self.capture_screenshot()
        success, state =  await self.process_screenshot(screenshot)
        return success, state

    async def capture_screenshot(self):
        return load_image('ffxiv1.jpg')  # Replace with capture_screenshot()

    async def process_screenshot(self, image):
        # Implementation to process the screenshot
        return await self.interactive_game_analyzer.analyze_screenshot(image)

    def get_latest_game_state(self):
        return self.latest_game_state