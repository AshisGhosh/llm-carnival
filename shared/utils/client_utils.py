import io
import httpx
from httpx import Timeout
from typing import Any, Dict, Optional
from PIL import Image

model_server_url = "http://model_server:8000"
timeout_default = 5.0

async def post_request(url: str, params: Dict[str, Any], files: Optional[Dict[str, Any]] = None, timeout: float = timeout_default) -> Dict[str, Any]:
    timeout = Timeout(timeout)
    print(f"Sending POST request to {url} with params: {params} and timeout: {timeout}")
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, params=params, files=files)
            response = response.json()
            response["success"] = True
            print(f"Response: {response}")
            return response
    except httpx.ReadTimeout as e:
        print(f"Timeout sending POST request to {url} with params: {params} and timeout: {timeout}: {e}")
        return {"success": False, "text": f"httpx.ReadTimeout: Timeout sending POST request to {url} with params: {params} and timeout: {timeout}: {e}"}
    except Exception as e:
        print(f"Error sending POST request to {url} with params: {params} and timeout: {timeout}: {e}")
        return {"success": False, "text": f"Error sending POST request to {url} with params: {params} and timeout: {timeout}: {e}"}


async def get_request(url: str) -> Dict[str, Any]:
    print(f"Sending GET request to {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(f"Response: {response.json()}")
        return response.json()

async def check_model_server_status() -> str:
    try:
        response = await get_request(model_server_url)
        return response
    except httpx.RequestError as e:
        print("Error checking model server status:", e)
        return False

async def generate_text_gpt2(prompt: str) -> str:
    response = await post_request(f"{model_server_url}/gpt2/generate-text", {"prompt": prompt})
    return response

async def process_image_blip(text: str, image: Image) -> Dict[str, Any]:
    timeout = 30.0

    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format="JPEG")
    image_byte_array = image_byte_array.getvalue()

    files = {'image': ('image.jpg', image_byte_array, 'image/jpeg')}
    params = {'text': text}
    response = await post_request(f"{model_server_url}/blip/process-image", params=params, files=files, timeout=timeout)
    return response


async def generate_text_gemma_2b_it(prompt: str, session_id: str = None) -> str:
    timeout = 60.0
    response = await post_request(f"{model_server_url}/gemma-2b-it/generate-text", {"prompt": prompt}, timeout=timeout)
    return response

async def clear_chat_history_gemma_2b_it(session_id: str = None) -> str:
    response = await post_request(f"{model_server_url}/gemma-2b-it/clear-chat-history", {"session_id": session_id})
    return response

