import uuid
from pymongo import MongoClient
import os
from dao.categoria_dao import get_or_create_categoria

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.tipos


def get_by_nombre(nombre: str):
    return collection.find_one(
        {"nombre": nombre},
        {"_id": 0}
    )

def get_or_create_tipo(nombre: str, categoria_nombre: str) -> str:
    categoria_id = get_or_create_categoria(categoria_nombre)

    tipo = collection.find_one({"nombre": nombre})
    if tipo:
        return tipo["id"]

    new_id = str(uuid.uuid4())

    collection.insert_one({
        "id": new_id,
        "nombre": nombre,
        "categoria_id": categoria_id
    })

    return new_id

def get_all_tipos():
    return list(collection.find({}, {"_id": 0}))

def update_tipo(id: int, tipo: str, categoria: str):
    tipo_id = get_or_create_tipo(tipo, categoria)
    collection.update_one(
        {"id": id},
        {"$set": {"tipo_id": tipo_id}}
    )