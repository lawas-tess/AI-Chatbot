from fastapi import FastAPI
from pydantic import BaseModel
from ai_router import chat_ai
from tracker import log_hours, progress

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "InternTrack API running"}

@app.post("/chat")
def chat(req: ChatRequest):
    return chat_ai(req.message)

@app.post("/log_hours")
def log(data: dict):
    return log_hours(data)

@app.get("/progress")
def get_progress(total: int, current: int):
    return progress(total, current)