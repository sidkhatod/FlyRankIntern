from fastapi import FastAPI, Body
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

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

# --- NEW STAGE 3 CODE BELOW ---

@app.post("/tasks", status_code=201)
def create_task(payload: dict = Body(...)):
    title = payload.get("title")
    
    # Validate the input: block missing or empty titles with a 400 Bad Request
    if not title or not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})
    
    # Calculate the next available ID
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    
    # Create the new task object
    new_task = {
        "id": new_id,
        "title": title,
        "done": False
    }
    
    # Save it to our memory list and return it
    tasks.append(new_task)
    return new_task


# --- NEW STAGE 4 CODE BELOW ---

@app.put("/tasks/{id}")
def update_task(id: int, payload: dict = Body(...)):
    # 1. Look for the task
    for i, task in enumerate(tasks):
        if task["id"] == id:
            title = payload.get("title")
            done = payload.get("done")
            
            # 2. Validate input if a title was provided
            if title is not None and not str(title).strip():
                return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
            
            # 3. Update the fields that were provided
            if title is not None:
                tasks[i]["title"] = title
            if done is not None:
                tasks[i]["done"] = done
                
            return tasks[i]
            
    # If the loop finishes without finding the task, return 404
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    # Look for the task and delete it if found
    for i, task in enumerate(tasks):
        if task["id"] == id:
            del tasks[i]
            return  # 204 No Content means we don't return a body
            
    # If not found, return 404
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})