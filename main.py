from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

app = FastAPI()

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


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.post("/tasks", status_code=201)
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


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON body"}
        )

    if not body:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    allowed_fields = {"title", "done"}

    if not any(field in body for field in allowed_fields):
        return JSONResponse(
            status_code=400,
            content={"error": "Body must contain title and/or done"}
        )

    if "title" in body:
        if not isinstance(body["title"], str) or body["title"].strip() == "":
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

    if "done" in body and not isinstance(body["done"], bool):
        return JSONResponse(
            status_code=400,
            content={"error": "Done must be true or false"}
        )

    for task in tasks:
        if task["id"] == task_id:
            if "title" in body:
                task["title"] = body["title"]

            if "done" in body:
                task["done"] = body["done"]

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )