from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27018"
DB_NAME = "arbres"
COLLECTION_NAME = "arbres"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
