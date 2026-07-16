# FlyRank Task API

A simple in-memory CRUD API for managing a to-do list, built with Python and FastAPI.

## How to Run

To start the server on localhost, run this command in your terminal:
`uvicorn main:app --reload`

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | API details |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get a specific task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |

## Example Request

**Command:**
`curl.exe -i http://localhost:8000/health`

**Response:**
(Paste the output of your curl command here!)

## Swagger UI

![Swagger UI Screenshot](swagger.png)