from fastapi import APIRouter, HTTPException
from app.embedding_context.application.covert_films_to_vector_handler import (
    covert_films_to_vector_handler,
)

router = APIRouter()


@router.post("/convert-films-to-vector")
def convert_films_to_vector():
    try:
        covert_films_to_vector_handler()
        return {"message": "Films converted to vector successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
