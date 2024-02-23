# shared/models/huggingface_llm.py
import asyncio

from transformers import pipeline, set_seed
from timeit import default_timer as timer

class HuggingFaceGPT2LLM:
    def __init__(self):
        self.initialized = False
    
    async def initialize(self):
        # Start the timer
        start_time = timer()
        self.generator = pipeline('text-generation', model='gpt2')
        # Stop the timer
        end_time = timer()
        print(f"HuggingFaceGPT2LLM initialized in {end_time - start_time:.2f} seconds")
        set_seed(1)
        self.num_return_sequences = 1
        self.max_length = 60
        self.initialized = True
    
    async def generate(self, prompt):
        if not self.initialized:
            asyncio.run(self.initialize())

        start_time = timer()
        response = self.generator(prompt, max_length=self.max_length, num_return_sequences=self.num_return_sequences)
        end_time = timer()
        print(f"LLM response generated from prompt length ({len(prompt)}) in {end_time - start_time:.2f} seconds")
        generated_text = response[0]['generated_text']
        print(f"LLM: {generated_text}")
        return generated_text