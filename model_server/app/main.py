from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI! This is the model server."}

@app.post("/generate-text")
async def generate_text(prompt: str):
    text = "hey there!"
    return {"text": text}