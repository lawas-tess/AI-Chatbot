from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["interntrack"]

hours_collection = db["hours"]
tasks_collection = db["tasks"]
chat_collection = db["chat"]
config_collection = db["config"]
reports_collection = db["reports"]