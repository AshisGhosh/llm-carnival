# shared/models/huggingface_gemma_2b_it.py
import os
import asyncio
from dotenv import load_dotenv
from timeit import default_timer as timer

from transformers import AutoTokenizer, AutoModelForCausalLM

load_dotenv()
MODEL_TOKEN = os.getenv("HF_TOKEN_GEMMA")

MAX_HISTORY = 10
class HuggingFaceGemma2BIt:
    def __init__(self):
        self.name = "HuggingFace-Gemma-2B-it"
        self.model_id = "google/gemma-2b-it"
        self.initialized = False
        self.chat_sessions = {}
        self.chat = []
    
    async def initialize(self):
        # Start the timer
        start_time = timer()
        print(f"Initializing {self.name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, token=MODEL_TOKEN)
        print("Tokenizer loaded.")
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id, token=MODEL_TOKEN)
        print("Model loaded.")
        # Stop the timer
        end_time = timer()
        print(f"{self.name} initialized in {end_time - start_time:.2f} seconds")
        self.initialized = True
    
    def update_chat_history(self, chat, new_message):
        if len(chat) >= MAX_HISTORY:
            chat.pop(0)
        chat.append(new_message)
        return chat

    def clear_chat_history(self, session_id=None):
        if session_id is not None:
            self.chat_sessions[session_id] = []
        else:
            self.chat = []
    
    def get_session_chat_history(self, session_id=None):
        if session_id in self.chat_sessions.keys():
            return self.chat_sessions[session_id]
        else:
            return []
    
    def update_session_chat_history(self, session_id, chat):
        if session_id is not None:
            self.chat_sessions[session_id] = chat
        else:
            self.chat = []
    
    async def generate(self, prompt, session_id=None):
        if not self.initialized:
            asyncio.run(self.initialize())
        
        self.chat = self.get_session_chat_history(session_id)

        print(f"Generating response from prompt length: {len(prompt)}")
        
        start_time = timer()
        self.chat =  self.update_chat_history(self.chat, {"role": "user", "content": prompt})
        
        prompt = self.tokenizer.apply_chat_template(self.chat, tokenize=False, add_generation_prompt=True)
        print(f"TOKENIZED Prompt: {prompt}")

        inputs = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")

        outputs = self.model.generate(inputs, max_new_tokens=100)
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        end_time = timer()

        generated_text = decoded_output.split('model\n')[-1].strip()
        print(f"{self.name} response generated from prompt length ({len(prompt)}) in {end_time - start_time:.2f} seconds")

        self.chat = self.update_chat_history(self.chat, {"role": "assistant", "content": generated_text})
        print(f"Generated text: {generated_text}")

        self.update_session_chat_history(session_id, self.chat)

        return generated_text