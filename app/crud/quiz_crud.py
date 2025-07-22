from sqlalchemy.orm import Session

from app.models.quiz_model import Quiz
from app.schemas.quiz_schema import QuizCreate


def create_quiz(db: Session, quiz: QuizCreate):
    new_quiz = Quiz(**quiz.dict())
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


def get_quiz(db: Session, quiz_id: int):
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def get_quizzes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Quiz).offset(skip).limit(limit).all()


def delete_quiz(db: Session, quiz_id: int):
    quiz = get_quiz(db, quiz_id)
    if quiz:
        db.delete(quiz)
        db.commit()
    return quiz
