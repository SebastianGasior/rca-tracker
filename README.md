---
`markdown
# RCA Tracker API

A simple FastAPI backend for recording and viewing incident reports.  
This project demonstrates backend development, testing, and containerisation with Docker.

---

## 🚀 Quick Start

### 1. Clone the repository
bash git clone https://github.com/SebastianGasior/rca-tracker.git cd rca-tracker
`

### 2. Create and activate a virtual environment
bash # Windows python -m venv .venv .\\.venv\\Scripts\\Activate.ps1 # macOS / Linux python3 -m venv .venv source .venv/bin/activate
### 3. Install dependencies
bash pip install -r requirements.txt
### 4. Run the API
bash uvicorn app.main:app --reload --port 8000
Then open:

* [http://localhost:8000/health](http://localhost:8000/health)
* [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI

---

## Endpoints

### Health Check

**GET** `/health`

* Confirms the API is live
  Response:
json {"status": "ok"}
### Incidents

**POST** `/incidents`
json { "title": "Example Incident", "severity": "P2", "description": "Demo issue" }
**GET** `/incidents`

* Returns all incidents currently stored in memory.

---

## Running Tests

Tests are located in the `tests/` folder.
bash pytest -v
Example output:
tests/test_api.py::test_health PASSED [100%]
---

## Running with Docker

Build and run the container:
bash docker build -t rca-tracker . docker run -p 8000:8000 rca-tracker
Then visit [http://localhost:8000/health](http://localhost:8000/health)

---

## Environment Variables

Example environment configuration (`.env.example`):
# Copy to .env and update values if needed # DATABASE_URL=mongodb://user:pass@host/db # SECRET_KEY=changeme # PORT=8000
---

## Project Purpose

This project is part of my software engineering portfolio.
It demonstrates the ability to design, build, and containerise a Python backend API using FastAPI and Docker.
It can easily be extended with a database (e.g. SQLite, Postgres, MongoDB) and a React frontend.

---

## Tech Stack

* Python 3.12
* FastAPI (backend framework)
* Uvicorn (ASGI server)
* Docker (containerisation)
* Pydantic (data validation)
* Pytest (testing)
* Black + Ruff (formatting and linting)

---

## Licence

MIT License © 2025 Sebastian Gasior

---

## Future Enhancements

* Add persistent storage (SQLite or MongoDB)
* Add user authentication (JWT)
* Add React frontend
* Deploy CI/CD pipeline via GitHub Actions
* Deploy public container to Azure

---