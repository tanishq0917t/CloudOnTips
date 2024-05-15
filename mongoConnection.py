from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from bson.objectid import ObjectId
import json

class MongoCollection:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def getCollection(cls,collectionName):
        with open("config.json","r") as config:
            data=json.load(config)
        username = data['mongoDB']['username']
        password = data['mongoDB']['password']
        cluster = data['mongoDB']['clusterID']

        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)
        uri=f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster}.mongodb.net/"

        client = MongoClient(uri, server_api=ServerApi('1'))

        db=client['CloudOnTips']
        collection=db[collectionName]
        return collection
    

# result = collection.insert_one(document)
# print(f"Inserted document ID: {result.inserted_id}")
# print(collection.find_one({"userid":""})['name'])

