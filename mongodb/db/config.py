# core modules
import os

# environment variables
MONGODB_CONNECTION_URI = os.getenv("MONGODB_CONNECTION_URI", "mongodb://localhost:27017")
MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME", "iteso")