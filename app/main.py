# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
# FastAPI provides the main tools for building an API quickly.
from fastapi import FastAPI
# Pydantic provides type checking and data validation for request/response models.
from pydantic import BaseModel
# List is a Python typing helper to declare a list of items.
from typing import List

# -------------------------------------------------------------
# INITIALISE APP
# -------------------------------------------------------------
# 'app' is our FastAPI instance. It represents the running web service.
# The title appears in the interactive API docs at /docs.
app = FastAPI(title="RCA Tracker API")

# -------------------------------------------------------------
# DATA MODELS
# -------------------------------------------------------------

# This model defines what the client (frontend or user) must send
# when creating a new incident.
class IncidentIn(BaseModel):
    title: str         # Short name of the incident, e.g. "Database latency"
    severity: str      # Severity level such as "P1", "P2", or "P3"
    description: str = ""  # Optional description (defaults to empty if not provided)

# This model defines what the server returns when sending data back.
# It includes an extra field 'id' generated automatically.
class Incident(IncidentIn):
    id: int            # Unique numeric ID assigned by the server


# -------------------------------------------------------------
# IN-MEMORY DATABASE
# -------------------------------------------------------------
# We’ll store incidents in a simple Python list (acting like a fake database).
# Every time the server restarts, this list resets.
# In a real project, this would be replaced with MongoDB, SQLite, or Postgres.
_DB: List[Incident] = []


# -------------------------------------------------------------
# ROUTES / ENDPOINTS
# -------------------------------------------------------------

# 1. Health Check
@app.get("/health")
def health():
    """
    Simple route to verify that the API is running.

    Example Request:
      GET /health

    Example Response:
      {
        "status": "ok"
      }
    """
    return {"status": "ok"}


# 2. Get all incidents
@app.get("/incidents", response_model=List[Incident])
def list_incidents():
    """
    Returns a list of all incidents currently stored in memory.

    Example Request:
      GET /incidents

    Example Response:
      [
        {
          "title": "Login error",
          "severity": "P2",
          "description": "Users cannot log in",
          "id": 1
        },
        {
          "title": "API timeout",
          "severity": "P1",
          "description": "External API not responding",
          "id": 2
        }
      ]
    """
    return _DB


# 3. Create a new incident
@app.post("/incidents", response_model=Incident, status_code=201)
def create_incident(payload: IncidentIn):
    """
    Adds a new incident to the list and returns it with an assigned ID.

    Steps:
      1. Receive JSON payload from client.
      2. Validate input matches IncidentIn model.
      3. Assign new ID = current number of incidents + 1.
      4. Store in in-memory list.
      5. Return the created incident as JSON.

    Example Request:
      POST /incidents
      {
        "title": "Database latency",
        "severity": "P1",
        "description": "High latency on database writes"
      }

    Example Response:
      {
        "title": "Database latency",
        "severity": "P1",
        "description": "High latency on database writes",
        "id": 3
      }
    """

    # Create a new Incident instance
    inc = Incident(id=len(_DB) + 1, **payload.model_dump())

    # Append it to our fake "database"
    _DB.append(inc)

    # Return the new incident as confirmation
    return inc
