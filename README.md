## AI vs Me

### My Prompt

I asked AI to build a Task CRUD API using Python and FastAPI with an in-memory list. The API had to support GET, POST, PUT, and DELETE operations, return the correct 200, 201, 204, 400, and 404 status codes, validate empty task titles, and provide Swagger UI documentation.

### Test Results

I tested the AI-generated version using the same requirements as my hand-built API.

- GET `/tasks` returned `200 OK`.
- POST `/tasks` returned `201 Created`.
- PUT `/tasks/{task_id}` returned `200 OK`.
- DELETE `/tasks/{task_id}` returned `204 No Content`.
- A missing task returned `404 Not Found`.
- An empty title returned `400 Bad Request`.

### What the AI Did Well

The AI generated a compact implementation of the core CRUD API. It correctly handled the CRUD operations and the HTTP status codes that I tested.

### What Was Different in My Version

My final hand-built version contains additional optional features that were not included in the AI-generated version:

- Filtering tasks using `?done=true` and `?done=false`
- Searching tasks using `?search=...`
- Combining filtering and search
- A `/stats` endpoint for total, completed, and open task counts

### What I Learned

Building the API myself first helped me understand routing, validation, HTTP status codes, error handling, and in-memory data. The AI could generate the core solution quickly, but testing and comparing both versions was still necessary to verify that the generated code actually met the requirements.