# shared/models/huggingface_vqa.py
import asyncio

from transformers import AutoProcessor, BlipForQuestionAnswering
from timeit import default_timer as timer

class HuggingFaceBLIPforVQA:
    def __init__(self):
        self.initialized = False
    
    async def initialize(self):
        # Start the timer
        start_time = timer()

        print("Initializing HuggingFaceBLIPforVQA...")
        self.model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        print("Model loaded.")
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-vqa-base")
        print("Processor loaded.")

        # Stop the timer
        end_time = timer()
        print(f"HuggingFaceBLIPforVQA initialized in {end_time - start_time:.2f} seconds")
        self.initialized = True

    async def process_image(self, text, image):
        if not self.initialized:
            asyncio.run(self.initialize())

        # Start the timer
        start_time = timer()

        # Process an image and return the model's output
        inputs = self.processor(images=image, text=text, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        generated_text = self.processor.decode(outputs[0], skip_special_tokens=True)
        print(f"VQA: {generated_text}")
        # Stop the timer
        end_time = timer()
        print(f"Image processed in {end_time - start_time:.2f} seconds")

        return generated_text

