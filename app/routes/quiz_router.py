from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.quiz_crud import create_quiz, delete_quiz, get_quiz, get_quizzes
from app.database import SessionLocal
from app.schemas.quiz_schema import QuizCreate, QuizOut

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=QuizOut)
def create_quiz_endpoint(quiz: QuizCreate, db: Session = Depends(get_db)):
    return create_quiz(db, quiz)


@router.get("/{quiz_id}", response_model=QuizOut)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = get_quiz(db, quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@router.get("/", response_model=list[QuizOut])
def list_quizzes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_quizzes(db, skip=skip, limit=limit)


@router.delete("/{quiz_id}")
def delete_quiz_endpoint(quiz_id: int, db: Session = Depends(get_db)):
    quiz = delete_quiz(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"detail": "Quiz deleted successfully"}
