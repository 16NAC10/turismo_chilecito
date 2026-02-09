import uuid
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.categorias
categorias = db.categorias
tipos = db.tipos


def create_categoria(nombre: str) -> str:
    nombre = nombre.strip()

    if not nombre:
        raise ValueError("El nombre de la categoría es obligatorio")

    existente = categorias.find_one(
        {"nombre": {"$regex": f"^{nombre}$", "$options": "i"}}
    )
    if existente:
        return existente["id_categoria"]

    new_id = str(uuid.uuid4())

    categorias.insert_one({
        "id_categoria": new_id,
        "nombre": nombre
    })

    return new_id


def update_categoria(categoria_id: str, data: dict) -> bool:
    update = {}

    if "nombre" in data:
        nombre = data["nombre"].strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        update["nombre"] = nombre

    if not update:
        return False

    result = categorias.update_one(
        {"id_categoria": categoria_id},
        {"$set": update}
    )

    return result.matched_count == 1


def get_or_create_categoria(nombre: str):
    cat = collection.find_one({"nombre": nombre})
    if cat:
        return cat["id_categoria"]

    new_id = str(uuid.uuid4())

    collection.insert_one({
        "id_categoria": new_id,
        "nombre": nombre
    })
    return new_id


def get_categoria(id: str):
    return collection.find_one(
        {"id_categoria": id},
        {"_id": 0}
    )


def get_all_categorias():
    return list(collection.find({}, {"_id": 0}))


def delete_categoria(categoria_id: str) -> bool:
    en_uso = tipos.count_documents({"categoria_id": categoria_id})

    if en_uso > 0:
        raise ValueError(
            f"No se puede eliminar la categoría: está asociada a {en_uso} tipo(s)"
        )

    result = categorias.delete_one({"id_categoria": categoria_id})
    return result.deleted_count == 1