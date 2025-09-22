# backend/database.py

import motor.motor_asyncio
from config import settings
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
db = client.bovilens_db

user_collection = db.get_collection("users")
analysis_collection = db.get_collection("analyses")