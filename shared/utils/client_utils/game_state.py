from typing import Dict, Any
from .http_client import post_request, get_request

from shared.tests.test_responses import get_dummy_game_state_response

GAME_STATE_SERVER_NAME = "http://game_state:8000"

async def get_game_state() -> Dict[str, Any]:
    return await get_request(f"{GAME_STATE_SERVER_NAME}/game_state/get_game_state")

async def get_dummy_game_state() -> Dict[str, Any]:
    return get_dummy_game_state_response()