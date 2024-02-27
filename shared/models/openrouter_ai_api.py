# shared/models/openrouter_ai_api.py
import os

from shared.utils.client_utils import post_request
from .chat_model import ChatModel

from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class OpenRouterAIAPI(ChatModel):
    def __init__(self):
        super().__init__("openrouter-ai-api", "OpenRouter AI API")
    
    async def initialize(self):
        self.initialized = True

    async def generate(self, messages, model):
        print(f"Generating text with OpenRouter AI API model: {model}")
        print(f"Messages: {messages}")
        headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        # "HTTP-Referer": YOUR_SITE_URL,  # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "llm-carnival",  # Optional. Shows in rankings on openrouter.ai.
        }

        data = {
            "model": model,  
            "messages": messages,
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "repetition_penalty": 1,
            "min_p": 0,
            "top_a": 0
            
        }

        model_server_url = "https://openrouter.ai/api/v1/chat/completions"
        response = await post_request(model_server_url, data=data, headers=headers)
        generated_text = response['choices'][0]['message']['content']
        return generated_text
