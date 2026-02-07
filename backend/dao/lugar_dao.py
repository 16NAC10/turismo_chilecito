from pymongo import MongoClient
import os
from dao.tipo_dao import get_or_create_tipo, get_by_nombre
from dao.servicio_dao import get_or_create_servicio
from dao.opinion_dao import delete_by_lugar
from dao.categoria_dao import get_by_nombre
import uuid

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.lugares

lugares = db.lugares
tipos = db.tipos
categorias = db.categorias


def new_uuid():
    return str(uuid.uuid4())


def get_or_create(collection, nombre):
    if nombre is None:
        return None

    doc = collection.find_one({"nombre": nombre})
    if doc:
        return doc["id"]

    nuevo = {
        "id": new_uuid(),
        "nombre": nombre
    }
    collection.insert_one(nuevo)
    return nuevo["id"]

def create_lugar(lugar: dict):
    tipo_id = get_or_create(tipos, lugar.get("tipo_nombre"))
    categoria_id = get_or_create(categorias, lugar.get("categoria_nombre"))

    doc = {
        "id": new_uuid(),
        "osm_id": lugar.get("osm_id"),
        "nombre": lugar.get("nombre"),
        "lat": lugar["lat"],
        "lon": lugar["lon"],
        "tipo_id": tipo_id,
        "categoria_id": categoria_id
    }

    lugares.update_one(
        {"osm_id": lugar.get("osm_id")},
        {"$setOnInsert": doc},
        upsert=True
    )
    
def get_all():
    return list(collection.find({}, {"_id": 0}))

def update_lugar(id: int, data: dict):
    update_data = {}

    if "nombre" in data:
        update_data["nombre"] = data["nombre"]

    if "lat" in data and "lon" in data:
        update_data["lat"] = data["lat"]
        update_data["lon"] = data["lon"]

    if update_data:
        collection.update_one(
            {"id": id},
            {"$set": update_data}
        )

def delete_lugar(id: int):
    # Cascada lógica: opiniones
    delete_by_lugar(id)

    # Eliminar lugar
    collection.delete_one({"id": id})

def get_by_tipo_nombre(tipo_nombre: str):
    tipo = get_by_nombre(tipo_nombre)

    if not tipo:
        return []

    return list(
        lugares.find(
            {"tipo_id": tipo["id"]},
            {"_id": 0}
        )
    )

def get_by_categoria_nombre(categoria_nombre: str):
    categoria = get_by_nombre(categoria_nombre)

    if not categoria:
        return []

    return list(
        lugares.find(
            {"categoria_id": categoria["id"]},
            {"_id": 0}
        )
    )

def get_by_servicio(servicio_id: int):
    return list(collection.find(
        {"servicios_ids": servicio_id},
        {"_id": 0}
    ))

def add_servicio(lugar_id: int, servicio_id: int):
    collection.update_one(
        {"id": lugar_id},
        {"$addToSet": {"servicios_ids": servicio_id}}
    )

def remove_servicio(lugar_id: int, servicio_id: int):
    collection.update_one(
        {"id": lugar_id},
        {"$pull": {"servicios_ids": servicio_id}}
    )