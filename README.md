# rca-tracker
FastAPI demo for incident tracking

# RCA Tracker API

A tiny FastAPI backend for recording and viewing incident reports. Good starter project to demonstrate Python APIs, data models, and basic CRUD.

## Quick start

1) Create a virtual environment and activate it
   - Windows (PowerShell)
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
   - macOS/Linux
     python3 -m venv .venv
     source .venv/bin/activate

2) Install dependencies
   pip install -r requirements.txt

3) Run the API
   uvicorn app.main:app --reload --port 8000

4) Open the interactive docs
   http://localhost:8000/docs

## Endpoints

GET /health  
Returns a simple status.

GET /incidents  
Returns all incidents currently held in memory.

POST /incidents  
Creates a new incident.

Example request body:
{
  "title": "Database latency",
  "severity": "P1",
  "description": "High latency on writes"
}

Example response:
{
  "title": "Database latency",
  "severity": "P1",
  "description": "High latency on writes",
  "id": 1
}

## Curl examples

Health:
curl http://localhost:8000/health

Create incident:
curl -X POST http://localhost:8000/incidents ^
  -H "content-type: application/json" ^
  -d "{ \"title\": \"DB lag\", \"severity\": \"P2\", \"description\": \"Spike\" }"

List incidents:
curl http://localhost:8000/incidents

## Notes

- Data is stored in memory for now – it resets when the server restarts.
- Next steps: add persistence (SQLite or MongoDB/Neon), simple auth, and tests.

