from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.embedding_context.application.retrieve_films_by_similarity import (
    retrieve_films_by_similarity,
)

router = APIRouter()


class LLMRequest(BaseModel):
    prompt: str


@router.post("/films/by-similarity")
def get_films_by_similarity(request: LLMRequest):
    try:
        response = retrieve_films_by_similarity(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
