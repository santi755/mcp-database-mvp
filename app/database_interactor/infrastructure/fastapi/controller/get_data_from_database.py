from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database_interactor.application.llm_handler import process_with_gemini

router = APIRouter()


class LLMRequest(BaseModel):
    prompt: str


@router.post("/llm/gemini")
def use_gemini_llm(request: LLMRequest):
    try:
        response = process_with_gemini(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
