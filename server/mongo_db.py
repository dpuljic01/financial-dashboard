import os
from flask_pymongo import pymongo

CONNECTION_STRING = os.getenv("MONGO_DB_CONNECTION_STRING")
client = pymongo.MongoClient(CONNECTION_STRING)
mongo_db = client.get_database("dp-finance")
