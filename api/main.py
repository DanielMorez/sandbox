from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import run

app = FastAPI(
    title="Sandbox API",
    description="API для запуска кода в Kubernetes-песочнице",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(run.router, prefix="/api", tags=["Run"])
