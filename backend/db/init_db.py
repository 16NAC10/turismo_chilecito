from pymongo import MongoClient
import os


def init_database():
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    db = client.turismo

    # =========================
    # COLECCIÓN: lugares
    # =========================
    lugares = db.lugares

    lugares.create_index(
        [("id", 1)],
        unique=True
    )

    lugares.create_index(
        [("osm_id", 1)],
        unique=True,
        partialFilterExpression={"osm_id": {"$exists": True}}
    )

    lugares.create_index([("tipo_id", 1)])
    lugares.create_index([("servicios_ids", 1)])
    lugares.create_index([("lat", 1), ("lon", 1)])

    # =========================
    # COLECCIÓN: tipos
    # =========================
    tipos = db.tipos

    tipos.create_index(
        [("id_tipo", 1)],
        unique=True
    )

    tipos.create_index(
        [("nombre", 1)],
        unique=True
    )

    tipos.create_index([("categoria_id", 1)])

    # =========================
    # COLECCIÓN: categorias
    # =========================
    categorias = db.categorias

    categorias.create_index(
        [("id_categoria", 1)],
        unique=True
    )

    categorias.create_index(
        [("nombre", 1)],
        unique=True
    )

    # =========================
    # COLECCIÓN: servicios
    # =========================
    servicios = db.servicios

    servicios.create_index(
        [("id_servicio", 1)],
        unique=True
    )

    servicios.create_index(
        [("nombre", 1)],
        unique=True
    )

    # =========================
    # COLECCIÓN: opiniones
    # =========================
    opiniones = db.opiniones

    opiniones.create_index(
        [("id_opinion", 1)],
        unique=True
    )

    opiniones.create_index([("lugar_id", 1)])

    opiniones.create_index(
        [("id_opinion", 1), ("lugar_id", 1)],
        unique=True
    )

    print("✅ Base de datos 'turismo' inicializada correctamente")


if __name__ == "__main__":
    init_database()
