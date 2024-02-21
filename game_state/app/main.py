from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI()

# Example route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}