import os
import time
import re
from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, sessionmaker

from google import genai

from models import Base, User, Project, Task
from schemas import TaskCreate, TaskResponse, QuickAddRequest


# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = Path(__file__).resolve().parent


# ==================================================
# ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Please configure DATABASE_URL in Render Environment Variables."
    )


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
        "Please configure GEMINI_API_KEY in Render Environment Variables."
    )


# ==================================================
# GEMINI CONFIGURATION
# ==================================================

GEMINI_MODEL = "gemini-3.6-flash"

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==================================================
# DATABASE CONNECTION
# ==================================================

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(
    bind=engine
)


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="TaskFlow Task API",
    version="0.1.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://task-flow-rtky.onrender.com",
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
# REQUEST LOGGING
# ==================================================

@app.middleware("http")
async def log_request(
    request: Request,
    call_next
):
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
# INSERTION SORT
# ==================================================

def insertion_sort(records, key):

    for i in range(
        1,
        len(records)
    ):

        current = records[i]

        j = i - 1

        while (
            j >= 0
            and records[j][key] > current[key]
        ):

            records[j + 1] = records[j]

            j -= 1

        records[j + 1] = current


# ==================================================
# BINARY SEARCH
# ==================================================

def binary_search(
    sorted_records,
    target_value,
    key
):

    low = 0
    high = len(sorted_records) - 1

    while low <= high:

        mid = (
            low + high
        ) // 2

        if (
            sorted_records[mid][key]
            == target_value
        ):
            return mid

        if (
            sorted_records[mid][key]
            < target_value
        ):

            low = mid + 1

        else:

            high = mid - 1

    return -1


# ==================================================
# LINEAR SEARCH
# ==================================================

def linear_search(
    records,
    target_value,
    key
):

    for i in range(
        len(records)
    ):

        if (
            records[i][key]
            == target_value
        ):
            return i

    return -1


# ==================================================
# COUNTING BENCHMARK
# ==================================================

def insertion_sort_count(
    records,
    key
):

    comparison_count = 0

    for i in range(
        1,
        len(records)
    ):

        current = records[i]

        j = i - 1

        while j >= 0:

            comparison_count += 1

            if (
                records[j][key]
                > current[key]
            ):

                records[j + 1] = records[j]

                j -= 1

            else:

                break

        records[j + 1] = current

    return comparison_count


def binary_search_count(
    sorted_records,
    target_value,
    key
):

    low = 0
    high = len(sorted_records) - 1

    comparison_count = 0

    while low <= high:

        mid = (
            low + high
        ) // 2

        comparison_count += 1

        if (
            sorted_records[mid][key]
            == target_value
        ):

            return {
                "index": mid,
                "comparison_count":
                    comparison_count
            }

        comparison_count += 1

        if (
            sorted_records[mid][key]
            < target_value
        ):

            low = mid + 1

        else:

            high = mid - 1

    return {
        "index": -1,
        "comparison_count":
            comparison_count
    }


def linear_search_count(
    records,
    target_value,
    key
):

    comparison_count = 0

    for i in range(
        len(records)
    ):

        comparison_count += 1

        if (
            records[i][key]
            == target_value
        ):

            return {
                "index": i,
                "comparison_count":
                    comparison_count
            }

    return {
        "index": -1,
        "comparison_count":
            comparison_count
    }


# ==================================================
# DETERMINISTIC TASK PARSER
# ==================================================

def mock_parse_task(
    description: str
):

    original = description

    working = description.lower()


    # --------------------------------------------------
    # PRIORITY
    # --------------------------------------------------

    high_keywords = [
        "urgent",
        "asap",
        "high priority"
    ]

    low_keywords = [
        "whenever",
        "low priority"
    ]


    if any(
        keyword in working
        for keyword in high_keywords
    ):

        priority = "high"

    elif any(
        keyword in working
        for keyword in low_keywords
    ):

        priority = "low"

    else:

        priority = "medium"


    # --------------------------------------------------
    # DUE DATE
    # --------------------------------------------------

    due_date_hint = None

    date_phrases = [
        "today",
        "tomorrow",
        "next week",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]


    for phrase in date_phrases:

        if phrase in working:

            due_date_hint = phrase

            break


    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    title = original

    priority_words_to_remove = [
        "urgent",
        "asap",
        "high priority",
        "whenever",
        "low priority"
    ]


    for keyword in (
        priority_words_to_remove
    ):

        pattern = re.compile(
            re.escape(keyword),
            re.IGNORECASE
        )

        title = pattern.sub(
            "",
            title
        )


    if due_date_hint is not None:

        pattern = re.compile(
            re.escape(due_date_hint),
            re.IGNORECASE
        )

        title = pattern.sub(
            "",
            title
        )


    title = title.strip()

    if not title:

        title = "Untitled task"


    return {
        "title": title,
        "priority": priority,
        "due_date_hint":
            due_date_hint
    }


# ==================================================
# AI CHAT - GEMINI
# ==================================================

@app.post("/ai/chat")
def ai_chat(data: dict):

    message = data.get(
        "message",
        ""
    ).strip()


    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message is required"
        )


    prompt = (
        "You are TaskFlow AI, an assistant "
        "inside a task management application.\n\n"
        "Help users with:\n"
        "- tasks\n"
        "- priorities\n"
        "- planning\n"
        "- productivity\n"
        "- project management\n\n"
        "Keep answers clear, useful and concise.\n\n"
        f"User: {message}"
    )


    try:

        response = (
            gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
        )


        answer = (
            response.text
            if response.text
            else "I could not generate a response."
        )


        return {
            "message": answer
        }


    except Exception as e:

        print(
            "========== GEMINI ERROR =========="
        )

        print(
            repr(e)
        )

        print(
            "=================================="
        )


        raise HTTPException(
            status_code=503,
            detail="AI service is currently unavailable."
        )


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():

    return {
        "message":
            "TaskFlow Task API is running"
    }


# ==================================================
# FRONTEND
# ==================================================

@app.get("/frontend")
def frontend():

    return FileResponse(
        BASE_DIR / "index.html"
    )


@app.get("/styles.css")
def styles():

    return FileResponse(
        BASE_DIR / "styles.css"
    )


@app.get("/script.js")
def script():

    return FileResponse(
        BASE_DIR / "script.js"
    )


# ==================================================
# CREATE TASK
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

    project = (
        db.query(Project)
        .filter(
            Project.id
            == task_data.project_id
        )
        .first()
    )


    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )


    task = Task(
        project_id=
            task_data.project_id,

        title=
            task_data.title,

        priority=
            task_data.priority,

        due_date=
            task_data.due_date
    )


    db.add(task)

    db.commit()

    db.refresh(task)


    return task


# ==================================================
# QUICK ADD TASK
# ==================================================

@app.post(
    "/tasks/quick-add",
    response_model=TaskResponse,
    status_code=201
)
def quick_add_task(
    request_data: QuickAddRequest,
    db: Session = Depends(get_db)
):

    parsed = mock_parse_task(
        request_data.description
    )


    title = parsed["title"]

    priority = parsed["priority"]

    due_date_hint = (
        parsed["due_date_hint"]
    )


    project = (
        db.query(Project)
        .filter(
            Project.id
            == request_data.project_id
        )
        .first()
    )


    if not project:

        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "type":
                        "value_error",

                    "loc": [
                        "body",
                        "project_id"
                    ],

                    "msg":
                        "Project does not exist",

                    "input":
                        request_data.project_id
                }
            ]
        )


    task_data = TaskCreate(
        project_id=
            request_data.project_id,

        title=title,

        priority=priority,

        due_date=due_date_hint
    )


    task = Task(
        project_id=
            task_data.project_id,

        title=
            task_data.title,

        priority=
            task_data.priority,

        due_date=
            task_data.due_date
    )


    db.add(task)


    try:

        db.commit()

        db.refresh(task)

    except Exception:

        db.rollback()

        raise


    return task


# ==================================================
# LIST TASKS + INSERTION SORT
# ==================================================

@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    status_code=200
)
def list_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db)
):

    tasks = (
        db.query(Task)
        .all()
    )


    records = [
        {
            "id": task.id,
            "project_id":
                task.project_id,
            "title":
                task.title,
            "priority":
                task.priority,
            "due_date":
                task.due_date
        }

        for task in tasks
    ]


    if sort == "priority":

        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3
        }


        for record in records:

            record["priority_rank"] = (
                priority_rank[
                    record["priority"]
                ]
            )


        insertion_sort(
            records,
            "priority_rank"
        )


        for record in records:

            del record[
                "priority_rank"
            ]


    elif sort is not None:

        raise HTTPException(
            status_code=400,
            detail="Unsupported sort option"
        )


    return records


# ==================================================
# SEARCH TASK
# ==================================================

@app.get(
    "/tasks/search",
    response_model=TaskResponse,
    status_code=200
)
def search_tasks(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):

    tasks = (
        db.query(Task)
        .all()
    )


    records = [
        {
            "id":
                task.id,

            "title":
                task.title
        }

        for task in tasks
    ]


    if algo == "binary":

        insertion_sort(
            records,
            "title"
        )


        index = binary_search(
            records,
            title,
            "title"
        )


    elif algo == "linear":

        index = linear_search(
            records,
            title,
            "title"
        )


    else:

        raise HTTPException(
            status_code=400,
            detail=
                "Algorithm must be binary or linear"
        )


    if index == -1:

        raise HTTPException(
            status_code=404,
            detail=
                "Task with exact title not found"
        )


    task_id = records[index]["id"]


    task = (
        db.query(Task)
        .filter(
            Task.id == task_id
        )
        .first()
    )


    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return task


# ==================================================
# GET TASK BY ID
# ==================================================

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id
        )
        .first()
    )


    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return task


# ==================================================
# UPDATE TASK
# ==================================================

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

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id
        )
        .first()
    )


    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    project = (
        db.query(Project)
        .filter(
            Project.id
            == task_data.project_id
        )
        .first()
    )


    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )


    task.project_id = (
        task_data.project_id
    )

    task.title = (
        task_data.title
    )

    task.priority = (
        task_data.priority
    )

    task.due_date = (
        task_data.due_date
    )


    db.commit()

    db.refresh(task)


    return task


# ==================================================
# DELETE TASK
# ==================================================

@app.delete(
    "/tasks/{task_id}",
    status_code=200
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id
        )
        .first()
    )


    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    db.delete(task)

    db.commit()


    return {
        "message":
            "Task deleted successfully"
    }


# ==================================================
# CREATE PROJECT
# ==================================================

@app.post(
    "/projects",
    status_code=201
)
def create_project(
    project_data: dict,
    db: Session = Depends(get_db)
):

    owner = (
        db.query(User)
        .filter(
            User.id
            == project_data["owner_id"]
        )
        .first()
    )


    if not owner:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    project = Project(
        name=
            project_data["name"],

        owner_id=
            project_data["owner_id"]
    )


    db.add(project)

    db.commit()

    db.refresh(project)


    return project


# ==================================================
# LIST PROJECTS
# ==================================================

@app.get(
    "/projects",
    status_code=200
)
def list_projects(
    db: Session = Depends(get_db)
):

    return (
        db.query(Project)
        .all()
    )


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

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id
        )
        .first()
    )


    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )


    result = (
        db.query(
            Project.id.label(
                "project_id"
            ),

            Project.name.label(
                "project_name"
            ),

            func.count(
                Task.id
            ).label(
                "task_count"
            )
        )

        .outerjoin(
            Task,
            Task.project_id
            == Project.id
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
        "project_id":
            result.project_id,

        "project_name":
            result.project_name,

        "task_count":
            result.task_count
    }


# ==================================================
# CREATE USER
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
        name=
            user_data["name"],

        email=
            user_data["email"]
    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return user


# ==================================================
# LIST USERS
# ==================================================

@app.get(
    "/users",
    status_code=200
)
def list_users(
    db: Session = Depends(get_db)
):

    return (
        db.query(User)
        .all()
    )