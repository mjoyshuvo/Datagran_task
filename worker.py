from celery import Celery
from utils import CustomJSONEncoder, get_db
from bson.objectid import ObjectId
import subprocess

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('task_worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task()
def task_executor(task_id):
    db = get_db()
    task_object_id = ObjectId(task_id)
    task = db.task_table.find_one({"_id": task_object_id})
    output = subprocess.getoutput(task['cmd'])
    print(output)
    db.task_table.update_one(
        {"_id": task_object_id},
        {"$set": {"status": "started", "output": output}}
    )
    return task_id
