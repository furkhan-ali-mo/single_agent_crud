import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Create client
client = MongoClient(MONGO_URI) #cluster level association via MongoDB object

# Reference to database
db = client[DB_NAME] #creating a DB if it already doesn't exist

# Reference to collection = like a datatable
users_collection = db["users"]
