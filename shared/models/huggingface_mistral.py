# shared/models/huggingface_mistral.py
import asyncio

from transformers import AutoModelForCausalLM, AutoTokenizer
from timeit import default_timer as timer

MAX_HISTORY = 10
class HuggingFaceMistral:
    def __init__(self):
        self.initialized = False
        self.model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.messages = []

    
    async def initialize(self):
        # Start the timer
        start_time = timer()
        print("Initializing HuggingFaceMistral...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        print("Tokenizer loaded.")
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id)
        print("Model loaded.")
        # Stop the timer
        end_time = timer()
        print(f"HuggingFaceMistral initialized in {end_time - start_time:.2f} seconds")
        self.initialized = True
    
    def update_chat_history(self, messages, new_message):
        if len(messages) >= MAX_HISTORY:
            messages.pop(0)
        messages.append(new_message)
        return messages

    def clear_chat_history(self):
        self.messages = []
    
    async def generate(self, prompt):
        if not self.initialized:
            asyncio.run(self.initialize())
        
        self.messages =  self.update_chat_history(self.messages, {"role": "user", "content": prompt})

        inputs = self.tokenizer.apply_chat_template(self.messages, return_tensors="pt").to("cpu")

        outputs = self.model.generate(inputs, max_new_tokens=20)
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        self.messages = self.update_chat_history(self.messages, {"role": "assistant", "content": generated_text})
        print(generated_text)
        return generated_text