from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.turismo
collection = db.opiniones

def create_opinion(opinion: dict):
    if collection.find_one({
        "lugar_id": opinion["lugar_id"],
        "id_opinion": opinion["id_opinion"]
    }):
        return

    collection.insert_one(opinion)

def get_by_lugar(lugar_id: int):
    return list(collection.find(
        {"lugar_id": lugar_id},
        {"_id": 0}
    ))

def delete_opinion(id_opinion: int):
    collection.delete_one({"id_opinion": id_opinion})

def get_promedio_por_lugar():
    return list(collection.aggregate([
        {
            "$group": {
                "_id": "$lugar_id",
                "promedio": {"$avg": "$puntuacion"},
                "cantidad": {"$sum": 1}
            }
        }
    ]))

def delete_by_lugar(lugar_id: int):
    collection.delete_many({"lugar_id": lugar_id})