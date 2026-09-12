# Task CRUD API

A simple REST API built with Python and FastAPI for managing tasks.

The API supports full CRUD operations using an in-memory Python list. It also includes optional features such as task filtering, searching, and task statistics.

## Features

- Create a new task
- List all tasks
- Get a single task by ID
- Update an existing task
- Delete a task
- Input validation
- Correct HTTP status codes
- Interactive Swagger UI documentation
- Filter tasks by completion status
- Search tasks by title
- View task statistics

## Installation

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

## Run the API

Start the server with:

```powershell
uvicorn main:app --reload
```

The API will run at:

`http://127.0.0.1:8000`

Swagger UI is available at:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{task_id}` | Get a task by ID | 200 |
| POST | `/tasks` | Create a new task | 201 |
| PUT | `/tasks/{task_id}` | Update an existing task | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |
| GET | `/stats` | Show task statistics | 200 |

Invalid request bodies return `400 Bad Request`.

Requests for task IDs that do not exist return `404 Not Found`.

## Example curl Response

Command:

```powershell
curl.exe -i http://127.0.0.1:8000/tasks/1
```

Example output:

```text
HTTP/1.1 200 OK
server: uvicorn
content-type: application/json

{"id":1,"title":"Learn Python","done":false}
```

## Optional Features

### Filter Tasks

Return only completed tasks:

```text
GET /tasks?done=true
```

Return only open tasks:

```text
GET /tasks?done=false
```

For example:

```powershell
curl.exe -i "http://127.0.0.1:8000/tasks?done=true"
```

### Search Tasks

Tasks can be searched by words contained in their titles.

Example:

```text
GET /tasks?search=python
```

Filtering and searching can also be combined:

```text
GET /tasks?done=false&search=python
```

For example:

```powershell
curl.exe -i "http://127.0.0.1:8000/tasks?done=false&search=python"
```

### Task Statistics

The stats endpoint calculates the total number of tasks, completed tasks, and open tasks.

```text
GET /stats
```

Example response:

```json
{
  "total": 3,
  "done": 1,
  "open": 2
}
```

## Swagger UI

FastAPI automatically generates interactive API documentation using Swagger UI.

The full CRUD cycle can be tested directly from the browser using the **Try it out** button.

![Swagger UI](swagger.png)

## Data Storage

This project uses an in-memory Python list for storing tasks.

There is no database or file-based storage. Because the data is stored only in memory, tasks created, updated, or deleted while the server is running are lost when the application restarts.