from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database_interactor.application.retrieve_films_from_prompt import (
    retrieve_films_from_prompt,
)

router = APIRouter()


class LLMRequest(BaseModel):
    prompt: str


@router.post("/llm/films")
def get_films_from_prompt(request: LLMRequest):
    try:
        response = retrieve_films_from_prompt(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
