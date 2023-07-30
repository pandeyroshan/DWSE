import datetime
import os
import random
import time

from celery import Celery
from db import update_weather_task

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task
def create_task(data):
    task_id = data["task_id"]
    task_type = data["task_type"]

    # Simulate a long-running task
    time.sleep(random.randint(1, 3) * int(task_type))

    # Update the task status
    data["status"] = "SUCCESS"
    data["result"] = random.uniform(1.0, 100.0)
    data["completed_at"] = datetime.datetime.now()

    # Update the task in the database
    update_weather_task(task_id, data)

    return True
