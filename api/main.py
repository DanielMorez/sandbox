from fastapi import FastAPI
from api.routers import run

app = FastAPI(
    title="Sandbox API",
    description="API для запуска кода в Kubernetes-песочнице",
    version="1.0.0"
)


app.include_router(run.router, prefix="/api", tags=["Run"])
