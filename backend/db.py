from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client["wheat_ai"]

users_collection = db["users"]
history_collection = db["history"]
