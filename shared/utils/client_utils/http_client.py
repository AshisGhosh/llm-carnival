import os
from typing import Any, Dict, Optional

import asyncio
import httpx
from httpx import Timeout
from PIL import Image

from dotenv import load_dotenv
load_dotenv()

TIMEOUT_DEFAULT = 5.0
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
