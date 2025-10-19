# Wenex API Service

This service handles all API endpoints and connects to Elasticsearch for storing and searching data.  
Access is secured using JWT tokens issued by the Auth Service.

---

## Prerequisites

- Docker (Desktop or Linux)
- Docker Compose
- Python 3.12+ (for local development)
- Auth Service running

---

## Setup

**Location:** `backend/api_service`

### 1. Navigate to service folder

```bash
cd backend/api_service

2. Create virtual environment (optional for local dev)

python -m venv .venv
source .venv/bin/activate    # Linux / WSL
.venv\Scripts\activate       # Windows PowerShell

3. Install dependencies
pip install -r requirements.txt
4. Environment variables
Create a .env file (optional for Docker Compose dev):
ELASTICSEARCH_URL=http://elasticsearch:9200
AUTH_SERVICE_URL=http://auth_service:5000
JWT_SECRET_KEY=human
Running with Docker Compose
We use two compose files:
dev-docker-compose.yml → API service (with hot reload for development)
es-docker-compose.yml → Elasticsearch service
Run both together

docker compose -f dev-docker-compose.yml -f es-docker-compose.yml up --build
Services & Ports

Elasticsearch → http://localhost:9200

FastAPI service → http://localhost:8000