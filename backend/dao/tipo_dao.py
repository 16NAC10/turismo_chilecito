import uuid
from pymongo import MongoClient
import os
from dao.categoria_dao import get_or_create_categoria

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.tipos
tipos = db.tipos
lugares = db.lugares


def new_uuid():
    return str(uuid.uuid4())


def create_tipo(nombre: str, categoria_nombre: str) -> str:
    if not nombre or len(nombre.strip()) < 2:
        raise ValueError("El nombre del tipo es inválido")

    categoria_id = get_or_create_categoria(categoria_nombre)

    existente = collection.find_one({
        "nombre": {"$regex": f"^{nombre}$", "$options": "i"}
    })

    if existente:
        raise ValueError("El tipo ya existe")

    tipo_id = new_uuid()

    collection.insert_one({
        "id_tipo": tipo_id,
        "nombre": nombre.strip(),
        "categoria_id": categoria_id
    })

    return tipo_id


def update_tipo(tipo_id: str, data: dict) -> bool:
    update_data = {}

    if "nombre" in data:
        nombre = data["nombre"].strip()
        if len(nombre) < 2:
            raise ValueError("Nombre inválido")
        update_data["nombre"] = nombre

    if "categoria_nombre" in data:
        categoria_id = get_or_create_categoria(data["categoria_nombre"])
        update_data["categoria_id"] = categoria_id

    if not update_data:
        return False

    result = collection.update_one(
        {"id_tipo": tipo_id},
        {"$set": update_data}
    )

    return result.matched_count > 0


def get_or_create_tipo(nombre: str, categoria_nombre: str) -> str:
    categoria_id = get_or_create_categoria(categoria_nombre)

    tipo = collection.find_one({"nombre": nombre})
    if tipo:
        return tipo["id_tipo"]

    new_id = str(uuid.uuid4())

    collection.insert_one({
        "id_tipo": new_id,
        "nombre": nombre,
        "categoria_id": categoria_id
    })

    return new_id


def get_tipo(id: str):
    return collection.find_one(
        {"id_tipo": id},
        {"_id": 0}
    )


def get_all_tipos():
    return list(collection.find({}, {"_id": 0}))


def delete_tipo(tipo_id: str) -> bool:
    en_uso = lugares.count_documents({"tipo_id": tipo_id})

    if en_uso > 0:
        raise ValueError(
            f"No se puede eliminar el tipo: está asociado a {en_uso} lugar(es)"
        )

    result = tipos.delete_one({"id_tipo": tipo_id})

    return result.deleted_count == 1


def get_tipos_by_categoria(categoria_id: str):
    return list(
        collection.find(
            {"categoria_id": categoria_id},
            {"_id": 0}
        )
    )