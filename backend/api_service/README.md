# Wenex API Service

This service handles all API endpoints and connects to Elasticsearch for storing and searching data. Access is secured using JWT tokens issued by the Auth Service.

---

## Prerequisites

* Docker (Desktop or Linux)
* Docker Compose
* Python 3.12+ (for local development)
* Auth Service running

---

## Setup

**Location:** `backend/api_service`

### 1. Navigate to service folder

```bash
cd backend/api_service
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

Create a `.env` file (if needed, optional for Docker Compose dev):

```env
ELASTICSEARCH_URL=http://elasticsearch:9200
AUTH_SERVICE_URL=http://auth_service:5000
JWT_SECRET_KEY=human
```

---

## Running with Docker Compose

```bash
docker-compose up -d
```

* Elasticsearch: `9200`
* FastAPI service: `8000`
* Ensure Auth Service is running on its network

### Test API Service

```bash
# Get data from API (requires JWT token from Auth Service)
curl -X GET http://localhost:8000/items \
-H "Authorization: Bearer <JWT_TOKEN>"
```

---

## Notes

* Elasticsearch data is stored in Docker container.
* API Service verifies JWT from Auth Service before allowing access.
* Use separate Docker Compose files for Auth and API services for modularity.
