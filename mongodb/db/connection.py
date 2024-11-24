# third-party modules
from pymongo import MongoClient

# custom modules
import mongodb.db.config as config 

mongoClient = MongoClient(config.MONGODB_CONNECTION_URI) # creates client for a MongoDB instance

database = mongoClient[config.MONGODB_DATABASE_NAME] # positions the client on the specified database