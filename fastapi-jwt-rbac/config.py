from dotenv import load_dotenv, mongodb
import os

# Load environment variables from .env file
load_dotenv()

# Access variables
mongo_uri = os.getenv("MONGO_URI")
secret_key = os.getenv("SECRET_KEY")
print(f"Connecting to MongoDB at {mongo_uri}")
