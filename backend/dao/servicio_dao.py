import uuid

from fastapi import HTTPException
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.servicios
servicios = db.servicios
lugares = db.lugares


def new_uuid():
    return str(uuid.uuid4())


def create_servicio(data: dict) -> str:
    nombre = data.get("nombre")

    if not nombre or not nombre.strip():
        raise ValueError("El nombre del servicio es obligatorio")

    existente = servicios.find_one(
        {"nombre": {"$regex": f"^{nombre}$", "$options": "i"}}
    )
    if existente:
        return existente["id_servicio"]

    nuevo = {
        "id_servicio": new_uuid(),
        "nombre": nombre.strip(),
        "descripcion": data.get("descripcion")
    }

    servicios.insert_one(nuevo)
    return nuevo["id_servicio"]

def get_or_create_servicio(nombre: str, descripcion: str | None = None) -> str:
    serv = collection.find_one({"nombre": nombre})
    if serv:
        return serv["id_servicio"]

    new_id = str(uuid.uuid4())

    collection.insert_one({
        "id_servicio": new_id,
        "nombre": nombre,
        "descripcion": descripcion
    })

    return new_id


def get_all_servicios():
    return list(collection.find({}, {"_id": 0}))


def get_by_id(servicio_id: str):
    return collection.find_one(
        {"id_servicio": servicio_id},
        {"_id": 0}
    )


def delete_servicio(servicio_id: str):
    usado = lugares.find_one(
        {"servicios_ids": servicio_id}
    )

    if usado:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el servicio porque está asignado a uno o más lugares"
        )

    result = servicios.delete_one({"id_servicio": servicio_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")