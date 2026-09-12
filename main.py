from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0"
)

tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Build FastAPI project", "done": False},
    {"id": 3, "title": "Practice CRUD", "done": True},
]


class TaskCreate(BaseModel):
    title: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.get("/", summary="Show API information")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Check API health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get a task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    if task.title is None or task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_id = max(t["id"] for t in tasks) + 1 if tasks else 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}", summary="Update an existing task")
def update_task(task_id: int, update: TaskUpdate):
    if not update.model_fields_set:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    if "title" in update.model_fields_set:
        if update.title is None or update.title.strip() == "":
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

    for task in tasks:
        if task["id"] == task_id:
            if "title" in update.model_fields_set:
                task["title"] = update.title

            if "done" in update.model_fields_set:
                task["done"] = update.done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )