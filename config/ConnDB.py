import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

MONGO_URI = os.getenv("MONGO_URI")

def get_db():
    if not MONGO_URI:
        raise Exception("MONGO_URI not set in .env file")
    return connect(host=MONGO_URI)

# Example usage:
# db = get_db()
