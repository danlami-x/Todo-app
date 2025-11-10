from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine, Base
import models
import schemas
import crud

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Todo App with MySQL")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Root
# ---------------------------
@app.get("/")
def root():
    return {"message": "Todo App is running"}


# ---------------------------
# User Endpoints
# ---------------------------
@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = crud.create_user(db, user)
    return new_user


@app.get("/users", response_model=List[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


# ---------------------------
# Task Endpoints
# ---------------------------
@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_task = crud.create_task(db, task, user_id)
    return new_task


@app.get("/tasks", response_model=List[schemas.TaskResponse])
def list_all_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.get("/tasks/user/{user_id}", response_model=List[schemas.TaskResponse])
def list_tasks_by_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_tasks_by_user_id(db, user_id)


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/tasks/{task_id}", response_model=schemas.TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task

