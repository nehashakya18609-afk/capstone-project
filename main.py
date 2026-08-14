
import time

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, sessionmaker

from models import Base, User, Project, Task
from schemas import TaskCreate, TaskResponse


# ==================================================
# DATABASE CONNECTION
# ==================================================

DATABASE_URL = "postgresql://postgres.ljnvxjbarkmigexidvws:radhekrishna18609@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="Capstone Task API"
)


# ==================================================
# CORS CONFIGURATION
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
           "http://127.0.0.1:8000",

    ],
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
    ],
    allow_credentials=True,
)


# ==================================================
# REQUEST LOGGING MIDDLEWARE
# ==================================================

@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (
        time.perf_counter() - start_time
    ) * 1000

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"- {process_time:.2f} ms"
    )

    return response


# ==================================================
# DATABASE DEPENDENCY
# ==================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():
    return {
        "message": "Capstone Task API is running"
    }


# ==================================================
# FRONTEND
# ==================================================

@app.get("/frontend")
def frontend():
    return FileResponse("index.html")


@app.get("/styles.css")
def styles():
    return FileResponse("styles.css")


@app.get("/script.js")
def script():
    return FileResponse("script.js")


# ==================================================
# TASKS
# ==================================================

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == task_data.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    task = Task(
        project_id=task_data.project_id,
        title=task_data.title,
        priority=task_data.priority,
        due_date=task_data.due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    status_code=200
)
def list_tasks(
    db: Session = Depends(get_db)
):
    return db.query(Task).all()


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200
)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    project = db.query(Project).filter(
        Project.id == task_data.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    task.project_id = task_data.project_id
    task.title = task_data.title
    task.priority = task_data.priority
    task.due_date = task_data.due_date

    db.commit()
    db.refresh(task)

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=200
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# ==================================================
# PROJECTS
# ==================================================

@app.post(
    "/projects",
    status_code=201
)
def create_project(
    project_data: dict,
    db: Session = Depends(get_db)
):
    owner = db.query(User).filter(
        User.id == project_data["owner_id"]
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    project = Project(
        name=project_data["name"],
        owner_id=project_data["owner_id"]
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@app.get(
    "/projects",
    status_code=200
)
def list_projects(
    db: Session = Depends(get_db)
):
    return db.query(Project).all()


# ==================================================
# PROJECT TASK STATISTICS
# ==================================================

@app.get(
    "/projects/{project_id}/task-statistics",
    status_code=200
)
def project_task_statistics(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    result = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
            func.count(Task.id).label("task_count")
        )
        .outerjoin(
            Task,
            Task.project_id == Project.id
        )
        .filter(
            Project.id == project_id
        )
        .group_by(
            Project.id,
            Project.name
        )
        .first()
    )

    return {
        "project_id": result.project_id,
        "project_name": result.project_name,
        "task_count": result.task_count
    }


# ==================================================
# USERS
# ==================================================

@app.post(
    "/users",
    status_code=201
)
def create_user(
    user_data: dict,
    db: Session = Depends(get_db)
):
    user = User(
        name=user_data["name"],
        email=user_data["email"]
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.get(
    "/users",
    status_code=200
)
def list_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()

