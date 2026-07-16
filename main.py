from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish internship assignment", "done": False},
    {"id": 3, "title": "Read API documentation", "done": True}
]

@app.get("/")
def read_root():
    """Returns basic information about the API."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    """Health check endpoint to confirm the server is running."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    """Retrieve the full list of all tasks."""
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    """Retrieve a single task by its ID."""
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.post("/tasks", status_code=201)
def create_task(payload: dict = Body(...)):
    """Create a new task by providing a title."""
    title = payload.get("title")
    if not title or not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})
    
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{id}")
def update_task(id: int, payload: dict = Body(...)):
    """Update an existing task's title or completion status."""
    for i, task in enumerate(tasks):
        if task["id"] == id:
            title = payload.get("title")
            done = payload.get("done")
            
            if title is not None and not str(title).strip():
                return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
            
            if title is not None:
                tasks[i]["title"] = title
            if done is not None:
                tasks[i]["done"] = done
                
            return tasks[i]
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    """Delete a task completely from the list."""
    for i, task in enumerate(tasks):
        if task["id"] == id:
            del tasks[i]
            return
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})