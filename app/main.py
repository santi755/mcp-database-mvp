from typing import Union
from app.shared.infrastructure.settings import get_settings

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    settings = get_settings()
    return {
        "mongodb_url": settings.mongodb_url,
        "google_api_key": settings.google_api_key,
    }


@app.post("/chat")
def chat(message: str):
    return {"message": message}
