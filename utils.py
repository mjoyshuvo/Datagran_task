import json
from bson import ObjectId
from pymongo import MongoClient


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def get_db():
    client = MongoClient(host='db',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource="admin")
    db = client["task_db"]
    return db
