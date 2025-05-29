from fastapi import APIRouter, HTTPException
from app.embedding_context.application.covert_films_to_vector_handler import (
    CovertFilmsToVectorHandler,
)

covert_films_to_vector_handler = CovertFilmsToVectorHandler()

router = APIRouter()


@router.post("/convert-films-to-vector")
def convert_films_to_vector():
    try:
        covert_films_to_vector_handler.handle()
        return {"message": "Films converted to vector successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
