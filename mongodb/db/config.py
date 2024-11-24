# core modules
import os

# third-party modules
from dotenv import load_dotenv

load_dotenv() # loads environment variables from .env file

# environment variables
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_NAME = os.getenv("MONGODB_NAME")