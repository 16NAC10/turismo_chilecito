from pymongo import MongoClient
import os
from dao.tipo_dao import get_or_create_tipo, get_tipo, get_tipos_by_categoria
from dao.servicio_dao import get_or_create_servicio
from dao.opinion_dao import delete_by_lugar
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
    tipo_id = get_or_create_tipo(
        lugar.get("tipo_nombre"),
        lugar.get("categoria_nombre")
    )

    doc = {
        "id": new_uuid(),
        "osm_id": lugar.get("osm_id"),
        "nombre": lugar.get("nombre"),
        "lat": lugar["lat"],
        "lon": lugar["lon"],
        "tipo_id": tipo_id,
        "servicios_ids": lugar.get("servicios", []),
        "source": lugar.get("source")
    }

    if lugar.get("source") == "OSM":
        lugares.update_one(
            {"osm_id": lugar["osm_id"]},
            {"$setOnInsert": doc},
            upsert=True
        )

    else:
        lugares.insert_one(doc)


def get_lugar(id: str):
    return collection.find_one(
        {"id": id},
        {"_id": 0}
    )


def get_all():
    return list(collection.find({}, {"_id": 0}))


def update_lugar(lugar_id: str, data: dict):
    update_data = {}

    if "nombre" in data:
        nombre = data["nombre"].strip()
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        update_data["nombre"] = nombre

    if "lat" in data:
        lat = data["lat"]
        if lat < -90 or lat > 90:
            raise ValueError("Latitud inválida")
        update_data["lat"] = lat

    if "lon" in data:
        lon = data["lon"]
        if lon < -180 or lon > 180:
            raise ValueError("Longitud inválida")
        update_data["lon"] = lon

    if "tipo_nombre" in data:
        tipo_id = get_or_create_tipo(
            data["tipo_nombre"],
            data.get("categoria_nombre")
        )
        update_data["tipo_id"] = tipo_id

    if not update_data:
        return False

    result = collection.update_one(
        {"id": lugar_id},
        {"$set": update_data}
    )

    return result.matched_count > 0


def delete_lugar(id: str):
    delete_by_lugar(id)
    collection.delete_one({"id": id})


def get_by_tipo(tipo_id: str):
    tipo = get_tipo(tipo_id)

    if not tipo:
        return []

    return list(
        lugares.find(
            {"tipo_id": tipo["id_tipo"]},
            {"_id": 0}
        )
    )


def get_by_categoria(categoria_id: str):
    tipos = get_tipos_by_categoria(categoria_id)

    if not tipos:
        return []

    tipo_ids = [t["id_tipo"] for t in tipos]

    return list(
        collection.find(
            {"tipo_id": {"$in": tipo_ids}},
            {"_id": 0}
        )
    )


def get_by_servicio(servicio_id: str):
    return list(
        lugares.find(
            {"servicios_ids": servicio_id},
            {"_id": 0}
        )
    )


def add_servicio(lugar_id: str, servicio_id: str):
    if not lugares.find_one({"id": lugar_id}):
        raise ValueError("Lugar no encontrado")

    lugares.update_one(
        {"id": lugar_id},
        {"$addToSet": {"servicios_ids": servicio_id}}
    )


def remove_servicio(lugar_id: str, servicio_id: str):
    if not lugares.find_one({"id": lugar_id}):
        raise ValueError("Lugar no encontrado")

    lugares.update_one(
        {"id": lugar_id},
        {"$pull": {"servicios_ids": servicio_id}}
    )


def update_servicios_lugar(lugar_id: str, servicios: list[str]):
    servicios_ids = [
        get_or_create_servicio(nombre)
        for nombre in servicios
    ]

    if not lugares.find_one({"id": lugar_id}):
        raise ValueError("Lugar no encontrado")

    lugares.update_one(
        {"id": lugar_id},
        {"$set": {"servicios_ids": servicios_ids}}
    )


def exists_lugar(lugar_id: str) -> bool:
    return collection.find_one({"id": lugar_id}) is not None