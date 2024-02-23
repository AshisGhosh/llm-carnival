from fastapi import FastAPI, File, UploadFile
from typing import IO
from PIL import Image

from shared.models.huggingface_llm import HuggingFaceGPT2LLM
from shared.models.huggingface_vqa import HuggingFaceBLIPforVQA

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI! This is the model server."}

@app.on_event("startup")
async def startup_event():
    app.llm = HuggingFaceGPT2LLM()
    await app.llm.initialize()
    app.vqa = HuggingFaceBLIPforVQA()
    await app.vqa.initialize()

@app.post("/generate-text")
async def generate_text(prompt: str):
    text = await app.llm.generate(prompt)
    return {"text": text}

@app.post("/process-image")
async def process_image(text: str, image_received: UploadFile = File(...)):
    try:
        image = Image.open(image_received.file)
    except Exception as e:
        return {"error": f"Error processing image: {e}"}
    
    answer = await app.vqa.process_image(text, image)
    return {"answer": answer}