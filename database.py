from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()  # To load the .env file

def init_db():
    # Use the MONGO_URI from the .env file
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/fastapi_rbac")
    connect(host=mongo_uri)

