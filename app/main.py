from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="Habit Tracker",
    description="Habit tracker API",
    version="1.0.0",
)

app.include_router(api_router)
