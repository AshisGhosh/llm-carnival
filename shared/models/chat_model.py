# shared/models/chat_model.py
import os
import asyncio
from timeit import default_timer as timer

from langfuse import Langfuse
langfuse = Langfuse()

MAX_HISTORY = 50

class ChatModel:
    def __init__(self, model_id, name=None):
        self.name = name
        self.model_id = model_id
        self.initialized = False
        self.chat_sessions = {}
        self.chat = []

    async def initialize(self):
        self.initialized = True
    
    def update_chat_history(self, chat, new_message):
        if len(chat) >= MAX_HISTORY:
            print(f"{self.name} - Chat history is full! Popping first message")
            chat.pop(0)
        chat.append(new_message)
        return chat

    def clear_chat_history(self, session_id=None):
        if session_id in self.chat_sessions.keys():
            self.chat_sessions[session_id] = []
        else:
            self.chat = []
    
    def get_session_chat_history(self, session_id=None):
        if session_id in self.chat_sessions.keys():
            return self.chat_sessions[session_id]
        else:
            if session_id not in [None, '']:
                trace = langfuse.trace(
                    id=session_id,
                    name=f"{self.model_id}-chat-history",
                    user_id="ashis",
                    model=self.model_id,
                    metadata=None
                )
            return []
    
    def update_session_chat_history(self, session_id, chat):
        if session_id not in [None, '']:
            self.chat_sessions[session_id] = chat
        else:
            self.chat = []
    
    async def generate(self, prompt, session_id=None):
        if not self.initialized:
            raise Exception("Chat model not initialized")
        return "Chat model response"

    async def generate_text(self, prompt, session_id=None, model=None):
        self.chat = self.get_session_chat_history(session_id)
        print(f"{self.name} - Received request with prompt: {prompt} and session_id: {session_id}")
        self.chat =  self.update_chat_history(self.chat, {"role": "user", "content": prompt})
        start_time = timer()
        if session_id:
            generation = langfuse.generation(
                trace_id=session_id,
                parent_observation_id=None,
                name="generate-text",
                model=model,
                model_parameters=None,
                input=self.chat,
                metadata=None
            )
        response = await self.generate(self.chat, model=model)
        if session_id:
            generation.end(output=generated_text)
        end_time = timer()
        print(f"{self.name} - Generated text in {end_time - start_time:.2f} seconds")
        if response[0]:
            generated_text = response[1]
            self.chat = self.update_chat_history(self.chat, {"role": "assistant", "content": generated_text})       
            self.update_session_chat_history(session_id, self.chat)
        return response
