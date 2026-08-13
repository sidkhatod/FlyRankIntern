import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the Task model using SQLModel
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = Field(default=False)

# Database Configuration for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@db:5432/tasks_db")
engine = create_engine(DATABASE_URL, echo=False)

# Lifespan logic to initialize the database
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Check if the table is completely empty
        first_task = session.exec(select(Task)).first()
        if not first_task:
            # Seed 3 example tasks
            session.add(Task(title="Buy groceries", done=False))
            session.add(Task(title="Finish internship assignment", done=False))
            session.add(Task(title="Read API documentation", done=True))
            session.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Dependency to get the DB session
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    """Returns basic information about the API."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    """Health check endpoint to confirm the server is running."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    """Retrieve the full list of all tasks."""
    return session.exec(select(Task)).all()

@app.get("/tasks/{id}")
def get_task(id: int, session: Session = Depends(get_session)):
    """Retrieve a single task by its ID."""
    task = session.get(Task, id)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    return task

@app.post("/tasks", status_code=201)
def create_task(payload: dict = Body(...), session: Session = Depends(get_session)):
    """Create a new task by providing a title."""
    title = payload.get("title")
    if not title or not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})
    
    new_task = Task(title=title, done=False)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

@app.put("/tasks/{id}")
def update_task(id: int, payload: dict = Body(...), session: Session = Depends(get_session)):
    """Update an existing task's title or completion status."""
    task = session.get(Task, id)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    
    title = payload.get("title")
    done = payload.get("done")
    
    if title is not None and not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
    
    if title is not None:
        task.title = title
    if done is not None:
        task.done = done
        
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int, session: Session = Depends(get_session)):
    """Delete a task completely from the list."""
    task = session.get(Task, id)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    
    session.delete(task)
    session.commit()
    return