import json
from utils import CustomJSONEncoder, get_db
from flask import Flask, jsonify, request
from worker import task_executor
from bson.objectid import ObjectId

app = Flask(__name__)


@app.route('/')
def ping_server():
    return "Welcome to the world of animals."


@app.route('/new_task', methods=['POST'])
def create_task():
    db = get_db()
    data = request.json
    if not data['cmd']:
        return {"status": 400, 'message': "Parameter 'cmd' is required"}
    payload = {
        "cmd": data['cmd'],
        "status": "not_started"
    }
    task_id = db.task_table.insert_one(payload).inserted_id
    response = {'id': task_id, 'status': 201}
    response_data = json.loads(CustomJSONEncoder().encode(response))
    task_executor.delay(response_data['id'])
    return response_data


@app.route('/get_output/<id>', methods=['GET'])
def get_task(id):
    db = get_db()
    task = db.task_table.find_one({"_id": ObjectId(id)})
    return json.loads(CustomJSONEncoder().encode(task))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
