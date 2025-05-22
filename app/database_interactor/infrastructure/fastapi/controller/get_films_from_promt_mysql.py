from fastapi import APIRouter
from pydantic import BaseModel
from app.database_interactor.application.retrieve_films_from_prompt_mysql import (
    retrieve_films_from_prompt_mysql,
)

router = APIRouter()


class LLMRequest(BaseModel):
    prompt: str


@router.post("/films/from-mysql")
async def get_films_from_promt_mysql(request: LLMRequest):
    films_response = retrieve_films_from_prompt_mysql(request.prompt)

    return {"data": films_response}
