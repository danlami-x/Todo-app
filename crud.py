from sqlalchemy.orm import Session
from models import User, Task
from schemas import UserCreate, TaskCreate, TaskUpdate
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------------
# User CRUD operations
# ---------------------------

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    safe_password = user.password[:72]
    hashed_password = pwd_context.hash(safe_password)

    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(User).all()

# ---------------------------
# Task CRUD operations
# ---------------------------

def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(
        title=task.title,
        description=task.description,
        is_completed=False,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks_by_user_id(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None

    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.is_completed is not None:
        db_task.is_completed = task_update.is_completed

    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task
