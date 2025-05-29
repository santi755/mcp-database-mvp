from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dishka.container import Container

from app.ai_context.infrastructure.dependency_injection.dependency_injection import (
    provider_ai_context,
)


def setup_container(app: FastAPI) -> Container:
    container = make_async_container(
        provider_ai_context,
    )
    setup_dishka(container, app)
    return container
