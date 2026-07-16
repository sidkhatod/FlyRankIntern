from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# 1. In-memory list of tasks
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish internship assignment", "done": False},
    {"id": 3, "title": "Read API documentation", "done": True}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# 2. Return the whole list of tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# 3 & 4. Return one task or a 404 error
@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
            
    # If the loop finishes and no task matches the ID, return a 404
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})