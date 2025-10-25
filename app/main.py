# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "rca-tracker")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "incidents")

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# -------------------------------------------------------------
# INITIALISE APP
# -------------------------------------------------------------
# 'app' is our FastAPI instance. It represents the running web service.
# The title appears in the interactive API docs at /docs.
app = FastAPI(title="RCA Tracker API")

# Allow requests from your Azure Static Web App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://black-sea-064252b03.3.azurestaticapps.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# DATA MODELS
# -------------------------------------------------------------


# Custom type for MongoDB's ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class IncidentIn(BaseModel):
    title: str
    severity: str
    description: str = ""

class Incident(IncidentIn):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Database latency",
                "severity": "P1",
                "description": "High latency on database writes",
                "_id": "507f1f77bcf86cd799439011"
            }
        }
        populate_by_name = True
        arbitrary_types_allowed = True


# -------------------------------------------------------------
# DATABASE CONNECTION EVENTS
# -------------------------------------------------------------
# Startup event to ensure database connection
@app.on_event("startup")
async def startup_db_client():
    """Validate database connection on startup"""
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        raise

# Shutdown event to close database connection
@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection"""
    client.close()


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
async def list_incidents():
    """Returns a list of all incidents from the database."""
    incidents = await collection.find().to_list(1000)
    return incidents


# 3. Create a new incident
@app.post("/incidents", response_model=Incident, status_code=201)
async def create_incident(incident: IncidentIn):
    """
    Creates a new incident in the database.
    
    Steps:
    1. Convert the incident to a dictionary
    2. Insert into MongoDB
    3. Return the created incident with its ID
    """
    incident_dict = incident.model_dump()
    result = await collection.insert_one(incident_dict)
    
    # Fetch the created document to return it
    created_incident = await collection.find_one({"_id": result.inserted_id})
    if created_incident is None:
        raise HTTPException(status_code=404, detail="Created incident not found")
    
    return created_incident
