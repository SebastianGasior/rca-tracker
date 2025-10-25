# RCA Tracker API

This project began as a small demo API using FastAPI and evolved into a **fully functional full-stack, production-grade cloud application**.  
The goal is to continuously enhance the system with new capabilities such as persistence, authentication, and monitoring — all while maintaining scalability, clean design, and DevOps best practices.

---

## 🧱 Current Architecture Overview

| Layer        | Stack                                     | Hosting               |
| ------------ | ----------------------------------------- | --------------------- |
| **Frontend** | React (Vite) + Bootstrap                  | Azure Static Web Apps |
| **Backend**  | FastAPI + Docker                          | Azure Container Apps  |
| **Database** | MongoDB Atlas (Free Tier)                 | Cloud                 |
| **CI/CD**    | GitHub Actions + Azure                    | Automatic deployments |
| **API CORS** | Configured for your Static Web App domain | ✅ Working             |


---

## 🌍 Live Full-Stack Demo
**Frontend (React + Bootstrap)**  
https://black-sea-064252b03.3.azurestaticapps.net  

**Backend (FastAPI + MongoDB)**  
https://rca-tracker.whiteocean-65212696.westeurope.azurecontainerapps.io/docs

---

## 🧠 Project Description
RCA Tracker API powers the backend logic for tracking and managing incident reports.  
It’s built with FastAPI, containerised with Docker, deployed on Azure Container Apps, and integrates with MongoDB Atlas for persistence.  
The API supports RESTful operations and serves as the data layer for the RCA Tracker React frontend.

---

## 🚀 Future Enhancements
- Add authentication and user management (JWT)  
- Include timestamps and advanced filtering  
- Integrate monitoring and logging  
- Improve CI/CD workflows  
- Extend API with analytics endpoints  
- Write unit tests and API integration tests

---


Quick local setup
------------------
1. Create a virtual environment and activate it (Windows PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the app (use the venv python):

```powershell
.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

3. Open http://localhost:8000/health and http://localhost:8000/docs

Testing
-------
Unit tests and a small end-to-end test are included in the `tests/` directory. To run all tests:

```powershell
.venv/Scripts/python.exe -m pytest -v
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
