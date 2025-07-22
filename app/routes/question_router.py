from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import question_model as QuestionModel
from app.schemas.question_schema import Question, QuestionCreate

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/", response_model=Question)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = QuestionModel(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
