from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="API Service", version="1.0")
app.include_router(router, prefix="/v1")
