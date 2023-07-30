import uuid
from db import (
    Base,
    create_weather_task,
    get_all_weather_tasks,
    get_weather_task_by_id,
)
from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from settings import settings
from sqlalchemy import create_engine
from worker import celery

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})

@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    weather_task_id = uuid.uuid4().hex
    task_data = {
        "task_type": payload["task_type"],
        "latitude": payload["latitude"],
        "longitude": payload["longitude"],
        "elevation": payload["elevation"],
        "task_id": weather_task_id
    }
    task = celery.send_task("worker.create_task", args=[task_data])
    task_data["celery_task_id"] = task.id,
    try:
        create_weather_task(task_data)
    except Exception as e:
        print(e)
        return JSONResponse({"message": "Error creating task in database."}, status_code=500)
    return JSONResponse({"task_id": task.id})

# get all tasks
@app.get("/tasks")
def get_tasks():
    return get_all_weather_tasks()

# get task by id
@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    return get_weather_task_by_id(task_id)

# get task status
@app.get("/tasks/{task_id}/status")
def get_task_status(task_id: str):
    weather_task = get_weather_task_by_id(task_id)
    res = celery.AsyncResult(task_id)
    if res.status == "SUCCESS":
        print(weather_task)
        return {
            "task_id": res.id,
            "status": res.status,
            "result": weather_task.result,
        }
    else:
        return {
            "task_id": res.id,
            "status": res.status,
            "result": None,
        }
