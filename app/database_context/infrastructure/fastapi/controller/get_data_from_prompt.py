from fastapi import APIRouter
from pydantic import BaseModel
from app.database_context.application.retrieve_data_from_prompt import (
    retrieve_data_from_prompt,
)

router = APIRouter()


class LLMRequest(BaseModel):
    prompt: str


@router.post("/from-mysql")
async def get_data_from_prompt(request: LLMRequest):
    data_response = retrieve_data_from_prompt(request.prompt)

    return {"data": data_response}
