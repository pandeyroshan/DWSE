from contextlib import contextmanager

from settings import settings
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

class ComputationalTask(Base):
    __tablename__ = "computational_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String)
    celery_task_id = Column(String)
    description = Column(String, index=True, nullable=True)
    latitude = Column(String)
    longitude = Column(String)
    elevation = Column(String)
    result = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())
    completed_at = Column(DateTime(timezone=True))
    status = Column(String, index=True, nullable=True)
    task_type = Column(Integer, index=True, nullable=True)

@contextmanager
def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create a weather task
def create_weather_task(task_data):
    new_task = ComputationalTask(**task_data)
    with get_db() as db:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

# Get Weather Task by celery task id
def get_weather_task_by_id(task_id):
    with get_db() as db:
        return db.query(ComputationalTask).filter(ComputationalTask.celery_task_id == task_id).first()

# update the task by task_id
def update_weather_task(task_id, updated_data):
    with get_db() as db:
        task = db.query(ComputationalTask).filter(ComputationalTask.task_id == task_id).first()
        if task:
            for key, value in updated_data.items():
                print("db", key, value)
                setattr(task, key, value)
            db.commit()
            db.refresh(task)
        return task

# delete a task by celery task id
def delete_weather_task(task_id):
    with get_db() as db:
        task = db.query(ComputationalTask).filter(ComputationalTask.celery_task_id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return task

# get all the tasks
def get_all_weather_tasks():
    with get_db() as db:
        return db.query(ComputationalTask).all()
