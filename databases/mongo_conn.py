from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv
student_collection = None
load_dotenv()

try:
    db_url = os.environ.get("DB_URL")
    
    if not db_url:
        raise ValueError("DB_URL is not set in environment variables.")
    
    conn = MongoClient(db_url, server_api=pymongo.server_api.ServerApi(
        version="1", strict=True, deprecation_errors=True
    ))

    conn.admin.command('ping')
    print("Database connected successfully!")
    db = conn["student_management_system"]
    student_collection = db["students"]

except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Database connection failed: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
