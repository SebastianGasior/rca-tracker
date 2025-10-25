# RCA Tracker API

A simple FastAPI backend for recording and viewing incident reports. This repo contains the API, tests, and deployment artifacts used to run the service on Azure Container Apps.

Live demo
-----------
The API is deployed on Azure Container Apps and available at:

https://rca-tracker.whiteocean-65212696.westeurope.azurecontainerapps.io

Key endpoints
- GET /health → returns API status (JSON)
- GET /incidents → list all incidents
- POST /incidents → create a new incident

Database Architecture
-------------------
The application uses Azure Cosmos DB with MongoDB API for persistent storage, providing:
- Scalable NoSQL database for storing incident reports
- MongoDB compatibility for easy development and testing
- Automatic indexing and fast queries
- High availability and global distribution capability

The data model stores incidents in a collection with fields for dates, descriptions, and incident details. Local development can use MongoDB directly, while production uses Cosmos DB.

Quick local setup
------------------
1. Create a virtual environment and activate it (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the app (use the venv python):

```powershell
C:/Users/sebas/OneDrive/Desktop/rca-tracker/.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

3. Open http://localhost:8000/health and http://localhost:8000/docs

Testing
-------
Unit tests and a small end-to-end test are included in the `tests/` directory. To run all tests:

```powershell
.../rca-tracker/.venv/Scripts/python.exe -m pytest -v
```

Deployment and Secrets
-----------------------------
For production, secrets like the MongoDB connection string are stored securely as Container App environment variables, not in source code or `.env` files. This keeps the implementation simple while maintaining security.

To set secrets in Azure Container Apps:
1. Navigate to your Container App in Azure Portal
2. Go to Configuration -> Environment Variables
3. Add your secrets as environment variables (e.g., MONGODB_URL)

Running in Docker
-----------------
Build and run locally:

```powershell
docker build -t rca-tracker .
docker run -p 8000:8000 rca-tracker
```

Environment variables
---------------------
The project reads `MONGODB_URL`, `DATABASE_NAME`, and `COLLECTION_NAME` from environment variables. Locally you can provide these in a `.env` file (do not commit `.env`). In Azure, these are configured as Container App environment variables.

Cleaning up test data
---------------------
If you want to remove the test incident created during the e2e run, you can either delete it directly from the database or I can add a small admin endpoint to remove test items.

Next steps (optional)
- Add more API endpoints for managing incidents
- Implement frontend UI
- Add user authentication if needed

---
MIT © 2025 Sebastian Gasior
