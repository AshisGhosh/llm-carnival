import os
import io
import uuid
from typing import Any, Dict, Optional

import asyncio
import httpx
from httpx import Timeout
from PIL import Image

from dotenv import load_dotenv
load_dotenv()

from langfuse import Langfuse
langfuse = Langfuse()

MODEL_SERVER_NAME = "http://model_server:8000"
TIMEOUT_DEFAULT = 5.0
SESSION_ID = str(uuid.uuid4())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


async def post_request(url: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None, timeout: float = TIMEOUT_DEFAULT) -> Dict[str, Any]:
    timeout = Timeout(timeout)
    print(f"Sending POST request to {url}:")
    print(f"    headers: {headers}")
    print(f"    params: {params}")
    print(f"    data: {data}")
    if files:
     print(f"    files len: {len(files)}")
    print(f"    timeout: {timeout}")

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, params=params, json=data, files=files, headers=headers, timeout=timeout)
            response = response.json()
            if not "success" in response.keys():
                response["success"] = True
            print(f"Response: {response}")
            return response
    except httpx.ReadTimeout as e:
        print(
            f"Timeout sending POST request to {url} with params: {params} and timeout: {timeout}: {e}")
        return {"success": False, "text": f"httpx.ReadTimeout: Timeout sending POST request to {url} with params: {params} and timeout: {timeout}: {e}"}
    except Exception as e:
        print(
            f"Error sending POST request to {url} with params: {params} and timeout: {timeout}: {e}")
        return {"success": False, "text": f"Error sending POST request to {url} with params: {params} and timeout: {timeout}: {e}"}


async def get_request(url: str) -> Dict[str, Any]:
    print(f"Sending GET request to {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(f"Response: {response.json()}")
        return response.json()


async def check_model_server_status() -> str:
    try:
        response = await get_request(MODEL_SERVER_NAME)
        return response
    except httpx.RequestError as e:
        print("Error checking model server status:", e)
        return False


async def generate_text_gpt2(prompt: str) -> str:
    response = await post_request(f"{MODEL_SERVER_NAME}/gpt2/generate-text", {"prompt": prompt})
    return response


async def process_image_blip(text: str, image: Image) -> Dict[str, Any]:
    timeout = 30.0

    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format="JPEG")
    image_byte_array = image_byte_array.getvalue()

    files = {'image': ('image.jpg', image_byte_array, 'image/jpeg')}
    params = {'text': text}
    response = await post_request(f"{MODEL_SERVER_NAME}/blip/process-image", params=params, files=files, timeout=timeout)
    return response


async def generate_text_gemma_2b_it(prompt: str, session_id: str = None) -> str:
    timeout = 60.0
    model_url = f"{MODEL_SERVER_NAME}/gemma-2b-it/generate-text"
    input = {"prompt": prompt, "session_id": session_id}
    response = await post_request(model_url, input, timeout=timeout)
    return response


async def clear_chat_history_gemma_2b_it(session_id: str = None) -> str:
    response = await post_request(f"{MODEL_SERVER_NAME}/gemma-2b-it/clear-chat-history", {"session_id": session_id})
    return response

async def generate_text_dummy(prompt: str) -> str:
    response = await post_request(f"{MODEL_SERVER_NAME}/dummy/generate-text", {"prompt": prompt})
    return response

async def generate_text_openrouter(prompt: str, session_id: str = None, model: str = "google/gemma-7b-it:free", attempts: int = 10) -> str:
    model_url = f"{MODEL_SERVER_NAME}/openrouter/generate-text"
    input = {"prompt": prompt, "session_id": session_id, "model": model}
    timeout = 60.0
    response = await post_request(model_url, input, timeout=timeout)
    if not response["success"]:
        if "code" in response['text'].keys() and response['text']["code"] == 429:
            attempts -= 1
            if attempts > 0:
                print(f"OpenRouter API rate limit exceeded. Retrying {attempts} more times.")
                # Wait 10 seconds before retrying
                await asyncio.sleep(10)
                response = await generate_text_openrouter(prompt, session_id=session_id, model=model, attempts=attempts)
            else:
                print(f"OpenRouter API rate limit exceeded. No more attempts.")
    return response