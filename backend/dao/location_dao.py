from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.lugares

def create_location(location: dict):
    collection.insert_one(location)

def get_all():
    return list(collection.find({}, {"_id": 0}))

def get_by_tipo(tipo: str):
    return list(collection.find({"tipo": tipo}, {"_id": 0}))

def update_location(id: int, data: dict):
    collection.update_one({"id": id}, {"$set": data})

def delete_location(id: int):
    collection.delete_one({"id": id})