from datetime import datetime
from database import hours_collection, tasks_collection

def log_hours(data):

    hours = int(data.get("hours", 0))
    task = data.get("task", "")

    hours_collection.insert_one({
        "hours": hours,
        "task": task,
        "logged_at": datetime.utcnow()
    })

    total_hours = sum(doc["hours"] for doc in hours_collection.find({}, {"hours": 1}))

    return {
        "message": "Hours logged successfully",
        "task": task,
        "hours_added": hours,
        "total_hours": total_hours
    }

def progress(total, current):

    total = int(total)
    current = int(current)

    percent = (current / total) * 100 if total else 0
    remaining = max(total - current, 0)

    return {
        "progress_percent": round(percent, 2),
        "remaining_hours": remaining
    }