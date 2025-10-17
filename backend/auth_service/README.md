# Wenex Auth Service

This service handles authentication (register/login) and issues JWTs for other services.

---

## Prerequisites

* Docker (Desktop or Linux)
* Docker Compose
* Python 3.10+ (for local development)
* Optional: Postman or curl for testing

---

## Setup

**Location:** `backend/auth_service`

### 1. Navigate to service folder

```bash
cd backend/auth_service
```

### 2. Create virtual environment (optional for local dev)

```bash
python -m venv .venv
source .venv/bin/activate    # Linux / WSL
.venv\Scripts\activate       # Windows PowerShell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Create a `.env` file (used by Docker Compose):

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/wenexdb
JWT_SECRET_KEY=human
FLASK_APP=app.py
FLASK_ENV=development
```

---

## Running with Docker Compose

```bash
docker-compose up -d
```

* Postgres: `5432`
* Flask Auth service: `5000`

### Test Auth Service

```bash
# Register a user
curl -X POST http://localhost:5000/register \
-H "Content-Type: application/json" \
-d '{"username":"testuser","password":"testpass"}'

# Login to get JWT token
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"testuser","password":"testpass"}'
```

---

## Notes

* Postgres data is persisted in Docker volume `postgres_data`.
* JWTs issued here are used by the API service to access protected endpoints.
