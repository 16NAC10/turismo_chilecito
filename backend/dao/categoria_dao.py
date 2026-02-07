from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.categorias

def get_by_nombre(nombre: str):
    return collection.find_one(
        {"nombre": nombre},
        {"_id": 0}
    )

def get_or_create_categoria(nombre: str):
    cat = collection.find_one({"nombre": nombre})
    if cat:
        return cat["id"]

    new_id = collection.count_documents({}) + 1
    collection.insert_one({
        "id": new_id,
        "nombre": nombre
    })
    return new_id

def get_all_categorias():
    return list(collection.find({}, {"_id": 0}))