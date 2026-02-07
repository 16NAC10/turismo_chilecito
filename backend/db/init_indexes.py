from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo

def create_indexes():
    db.lugares.create_index("id", unique=True)
    db.lugares.create_index("tipo_id")
    db.lugares.create_index("servicios_ids")

    db.opiniones.create_index("lugar_id")

    db.tipos.create_index("nombre", unique=True)

    db.servicios.create_index("nombre", unique=True)

if __name__ == "__main__":
    create_indexes()
    print("Índices creados correctamente")
