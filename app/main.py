from typing import Union
from app.shared.infrastructure.settings import get_settings

from fastapi import FastAPI
from app.database_interactor.infrastructure.fastapi.controller.get_data_from_database import (
    router as gemini_router,
)

app = FastAPI()

app.include_router(gemini_router)


@app.get("/")
def read_root():
    settings = get_settings()
    return {
        "mongodb_url": settings.mongodb_url,
        "google_api_key": settings.google_api_key,
    }
