# third-party modules
from pymongo import MongoClient

# custom modules
import mongodb.db.config as config 

mongoClient = MongoClient(config.MONGODB_URI) # creates client for a MongoDB instance

database = mongoClient[config.MONGODB_NAME] # positions the client on the specified database