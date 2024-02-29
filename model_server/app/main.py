from fastapi import FastAPI, File, UploadFile
from typing import Optional
from PIL import Image

from shared.models.huggingface_gpt2 import HuggingFaceGPT2
from shared.models.huggingface_vqa import HuggingFaceBLIPforVQA
from shared.models.huggingface_mistral import HuggingFaceMistral
from shared.models.huggingface_gemma_2b_it import HuggingFaceGemma2BIt
from shared.models.openrouter_ai_api import OpenRouterAIAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI! This is the model server."}

@app.on_event("startup")
async def startup_event():
    app.gpt2 = HuggingFaceGPT2()
    await app.gpt2.initialize()
    app.vqa = HuggingFaceBLIPforVQA()
    await app.vqa.initialize()
    # app.mistral = HuggingFaceMistral() # way too large
    # await app.mistral.initialize()
    app.gemma_2b_it = None
    app.openrouter = OpenRouterAIAPI()
    await app.openrouter.initialize()

@app.post("/gpt2/generate-text")
async def generate_text_gpt2(prompt: str):
    text = await app.gpt2.generate(prompt=prompt)
    return {"success": True, "text": text}

@app.post("/blip/process-image")
async def process_image(text: str, image: UploadFile = File(...)):
    try:
        image = Image.open(image.file)
    except Exception as e:
        return {"error": f"Error processing image: {e}"}
    
    answer = await app.vqa.process_image(text, image)
    return {"success": True, "answer": answer}

# @app.post("/mistral/generate-text")
# async def generate_text_mistral(prompt: str):
#     text = await app.mistral.generate(prompt)
#     return {"text": text}

# @app.post("/mistral/clear-chat-history")
# async def clear_chat_history():
#     app.mistral.clear_chat_history()
#     return {"message": "Chat history cleared."}

@app.post("/gemma-2b-it/generate-text")
async def generate_text_gemma_2b_it(prompt: str, session_id: Optional[str] = None):
    if app.gemma_2b_it is None:
        app.gemma_2b_it = HuggingFaceGemma2BIt()
        await app.gemma_2b_it.initialize()
    print(f'Received request for gemma-2b-it with prompt: {prompt} and session_id: {session_id}')
    text = await app.gemma_2b_it.generate(prompt=prompt, session_id=session_id)
    return {"success": True, "text": text}

@app.post("/gemma-2b-it/clear-chat-history")
async def clear_chat_history(session_id: Optional[str] = None):
    app.gemma_2b_it.clear_chat_history(session_id=session_id)
    return {"success": True, "message": "Chat history cleared."}

@app.post("/dummy/generate-text")
async def generate_text_dummy(prompt: str):
    return {"text": f"Dummy response to prompt: {prompt}"}

@app.post("/openrouter/generate-text")
async def generate_text_openrouter(prompt: str, session_id: Optional[str] = None, model: Optional[str] = "google/gemma-7b-it:free"):
    success, text = await app.openrouter.generate_text(prompt=prompt, session_id=session_id, model=model)
    return {"success": success, "text": text}