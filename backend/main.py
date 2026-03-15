from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
from ai_router import chat_ai
from tracker import log_hours, progress
from database import chat_collection, config_collection, reports_collection

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None

@app.get("/")
def root():
    return {"status": "InternTrack API running"}

@app.post("/chat")
def chat(req: ChatRequest):
    return chat_ai(req.message, req.history)

@app.post("/log_hours")
def log(data: dict):
    return log_hours(data)

@app.get("/progress")
def get_progress(total: int, current: int):
    return progress(total, current)

@app.post("/save_config")
def save_config(data: dict):
    config_collection.update_one({}, {"$set": data}, upsert=True)
    return {"message": "Config saved"}

@app.get("/get_config")
def get_config():
    config = config_collection.find_one({}, {"_id": 0})
    return config or {}

@app.get("/chat_history/{route}")
def get_chat_history(route: str):
    docs = list(chat_collection.find({"route": route}, {"_id": 0}).sort("timestamp", 1))

    history = []
    for doc in docs:
        user_message = doc.get("user")
        assistant_message = doc.get("assistant")

        if user_message:
            history.append({"role": "user", "content": user_message})
        if assistant_message:
            history.append({"role": "assistant", "content": assistant_message})

    return {"messages": history}

@app.post("/reports")
def save_report(data: dict):
    data.setdefault("report_id", str(uuid4()))
    reports_collection.insert_one(data)
    return {"message": "Report saved", "report_id": data["report_id"]}

@app.get("/reports")
def get_reports():
    reports = list(
        reports_collection.find({}, {"_id": 0}).sort("created_at", -1)
    )
    return {"reports": reports}

@app.delete("/reports/{report_id}")
def delete_report(report_id: str):
    result = reports_collection.delete_one({"report_id": report_id})
    return {"deleted": result.deleted_count == 1}