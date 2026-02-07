from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.servicios

def get_or_create_servicio(nombre: str):
    serv = collection.find_one({"nombre": nombre})
    if serv:
        return serv["id"]

    new_id = collection.count_documents({}) + 1
    collection.insert_one({
        "id": new_id,
        "nombre": nombre
    })
    return new_id

def get_all_services():
    return list(collection.find({}, {"_id": 0}))

def update_servicios(id: int, servicios: list[str]):
    servicios_ids = [
        get_or_create_servicio(s)
        for s in servicios
    ]

    collection.update_one(
        {"id": id},
        {"$set": {"servicios_ids": servicios_ids}}
    )