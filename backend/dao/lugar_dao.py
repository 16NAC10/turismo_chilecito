from pymongo import MongoClient
import os
from dao.tipo_dao import get_or_create_tipo
from dao.servicio_dao import get_or_create_servicio
from dao.opinion_dao import delete_by_lugar
import uuid

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.lugares

lugares = db.lugares
tipos = db.tipos
categorias = db.categorias
servicios = db.servicios


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


def create_lugar(lugar: dict) -> str:

    nombre = lugar.get("nombre")
    lat = lugar.get("lat")
    lon = lugar.get("lon")
    source = lugar.get("source", "MANUAL")

    if not nombre or not nombre.strip():
        raise ValueError("El nombre es obligatorio")

    nombre = nombre.strip()

    if lat is None:
        raise ValueError("La latitud es obligatoria")

    if lon is None:
        raise ValueError("La longitud es obligatoria")

    if not (-90 <= lat <= 90):
        raise ValueError("Latitud inválida")

    if not (-180 <= lon <= 180):
        raise ValueError("Longitud inválida")

    if source == "MANUAL":

        if lugares.find_one({
            "nombre": nombre,
            "source": "MANUAL"
        }):

            raise ValueError(
                f"Ya existe un lugar manual con el nombre '{nombre}'"
            )

    doc = {

        "id": new_uuid(),

        "nombre": nombre,

        "lat": lat,

        "lon": lon,

        "source": source

    }

    if source == "OSM" and lugar.get("osm_id"):

        doc["osm_id"] = lugar["osm_id"]

    tipo_nombre = lugar.get("tipo_nombre")
    categoria_nombre = lugar.get("categoria_nombre")

    if tipo_nombre and categoria_nombre:

        tipo_id = get_or_create_tipo(
            tipo_nombre,
            categoria_nombre
        )

        tipo = tipos.find_one(
            {"id_tipo": tipo_id},
            {"_id": 0}
        )

        categoria = categorias.find_one(
            {"id_categoria": tipo["categoria_id"]},
            {"_id": 0}
        )

        doc["tipo"] = {

            "id_tipo": tipo["id_tipo"],
            "nombre": tipo["nombre"],

            "categoria": {

                "id_categoria": categoria["id_categoria"],
                "nombre": categoria["nombre"]

            }

        }

    servicios_input = lugar.get("servicios")

    if servicios_input:

        servicios_embebidos = []

        for nombre_servicio in servicios_input:

            servicio_id = get_or_create_servicio(
                nombre_servicio
            )

            servicio = servicios.find_one(
                {"id_servicio": servicio_id},
                {"_id": 0}
            )

            servicios_embebidos.append({

                "id_servicio": servicio["id_servicio"],
                "nombre": servicio["nombre"]

            })

        if servicios_embebidos:

            doc["servicios"] = servicios_embebidos

    if lugar.get("osm"):

        doc["osm"] = lugar["osm"]

    if source == "OSM":

        lugares.update_one(

            {"osm_id": doc["osm_id"]},

            {"$setOnInsert": doc},

            upsert=True
        )

    else:

        lugares.insert_one(doc)

    return doc["id"]


def get_lugar(id: str):
    return collection.find_one(
        {"id": id},
        {"_id": 0}
    )


def get_all():
    return list(collection.find({}, {"_id": 0}))


def update_lugar(lugar_id: str, data: dict) -> bool:

    lugar = lugares.find_one({"id": lugar_id})

    if not lugar:
        raise ValueError("Lugar no encontrado")

    update_data = {}

    if "nombre" in data:

        nombre = data["nombre"]

        if not nombre or not nombre.strip():

            raise ValueError("El nombre no puede estar vacío")

        nombre = nombre.strip()

        if lugar.get("source") == "MANUAL":

            existe = lugares.find_one({

                "nombre": nombre,

                "source": "MANUAL",

                "id": {"$ne": lugar_id}

            })

            if existe:

                raise ValueError(
                    "Ya existe un lugar manual con ese nombre"
                )

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

    tipo_nombre = data.get("tipo_nombre")
    categoria_nombre = data.get("categoria_nombre")

    if tipo_nombre and categoria_nombre:

        tipo_id = get_or_create_tipo(

            tipo_nombre,

            categoria_nombre

        )

        tipo = tipos.find_one(

            {"id_tipo": tipo_id},

            {"_id": 0}

        )

        categoria = categorias.find_one(

            {"id_categoria": tipo["categoria_id"]},

            {"_id": 0}

        )

        update_data["tipo"] = {

            "id_tipo": tipo["id_tipo"],

            "nombre": tipo["nombre"],

            "categoria": {

                "id_categoria": categoria["id_categoria"],

                "nombre": categoria["nombre"]

            }

        }

    if not update_data:

        return False

    result = lugares.update_one(

        {"id": lugar_id},

        {"$set": update_data}

    )

    return result.modified_count > 0


def delete_lugar(lugar_id: str) -> bool:

    lugar = lugares.find_one({"id": lugar_id})

    if not lugar:

        return False

    delete_by_lugar(lugar_id)
    result = lugares.delete_one({"id": lugar_id})

    return result.deleted_count > 0


def get_by_tipo(tipo_nombre: str):

    return list(

        lugares.find(

            {"tipo.nombre": tipo_nombre},

            {"_id": 0}
        )
    )


def get_by_categoria(categoria_nombre: str):

    return list(

        lugares.find(

            {"tipo.categoria.nombre": categoria_nombre},

            {"_id": 0}
        )
    )


def get_by_servicio(servicio_id: str):

    return list(
        lugares.find(
            {
                "servicios.id_servicio": {
                    "$regex": f"^{servicio_id}$",
                    "$options": "i"
                }
            },
            {"_id": 0}
        )
    )


def add_servicio(lugar_id: str, servicio_id: str):

    lugar = lugares.find_one({"id": lugar_id})

    if not lugar:

        raise ValueError("Lugar no encontrado")

    servicio = servicios.find_one(
        {"id_servicio": servicio_id},
        {"_id": 0}
    )

    lugares.update_one(
        {
            "id": lugar_id,
            "servicios.id_servicio": {
                "$ne": servicio_id
            }
        },
        {
            "$push": {
                "servicios": servicio
            }
        }
    )


def remove_servicio(lugar_id: str, servicio_id: str):

    result = lugares.update_one(
        {"id": lugar_id},
        {
            "$pull": {
                "servicios": {
                    "id_servicio": servicio_id
                }
            }
        }
    )

    if result.matched_count == 0:
        raise ValueError("Lugar no encontrado")


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