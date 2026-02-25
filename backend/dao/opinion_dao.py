from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.opiniones
lugares = db.lugares


def create_opinion(opinion: dict):
    if not lugares.find_one({"id": opinion["lugar_id"]}):
        raise ValueError("El lugar no existe")

    if collection.find_one({"id_opinion": opinion["id_opinion"]}):
        return False

    collection.insert_one(opinion)
    return True


def get_by_lugar(lugar_id: str):
    return list(
        collection.find(
            {"lugar_id": lugar_id},
            {"_id": 0}
        )
    )


def delete_opinion(id_opinion: str) -> bool:
    result = collection.delete_one({"id_opinion": id_opinion})
    return result.deleted_count == 1


def get_promedio_by_lugar(lugar_id: str):

    resultado = list(collection.aggregate([

        {
            "$match": {
                "lugar_id": lugar_id
            }
        },

        {
            "$group": {
                "_id": "$lugar_id",
                "promedio": {"$avg": "$puntuacion"},
                "cantidad": {"$sum": 1}
            }
        },

        {
            "$project": {
                "_id": 0,
                "lugar_id": "$_id",
                "promedio": {"$round": ["$promedio", 2]},
                "cantidad": 1
            }
        }

    ]))

    return resultado[0] if resultado else None


def delete_by_lugar(lugar_id: str):
    collection.delete_many({"lugar_id": lugar_id})