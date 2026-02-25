from pymongo import MongoClient
import os


def init_database():

    client = MongoClient(
        os.getenv("MONGO_URI", "mongodb://localhost:27017")
    )

    db = client.turismo

    # =====================================================
    # COLECCIÓN: lugares (DOCUMENTAL)
    # =====================================================

    lugares = db.lugares

    lugares.create_index(
        [("id", 1)],
        unique=True
    )

    lugares.create_index(
        [("osm_id", 1)],
        unique=True,
        partialFilterExpression={
            "osm_id": {"$exists": True}
        }
    )

    lugares.create_index(
        [("nombre", 1)],
        partialFilterExpression={
            "source": "MANUAL"
        }
    )

    lugares.create_index(
        [("tipo.id_tipo", 1)]
    )

    lugares.create_index(
        [("tipo.categoria.id_categoria", 1)]
    )

    lugares.create_index(
        [("servicios.id_servicio", 1)]
    )

    lugares.create_index(
        [("lat", 1), ("lon", 1)]
    )

    lugares.create_index(
        [("source", 1)]
    )

    # =====================================================
    # COLECCIÓN: opiniones
    # =====================================================

    opiniones = db.opiniones

    opiniones.create_index(
        [("id_opinion", 1)],
        unique=True
    )

    opiniones.create_index(
        [("lugar_id", 1)]
    )

    print("Base de datos inicializada correctamente")


if __name__ == "__main__":

    init_database()