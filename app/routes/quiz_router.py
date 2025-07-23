from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db_connection import get_db
from app.dtos.question import QuizCreate
from app.models.quiz_model import Quiz

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.post("/")
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    new_quiz = Quiz(
        title=quiz.title,
        course_id=quiz.course_id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return {"message": "Quiz created", "quiz_id": new_quiz.id}
