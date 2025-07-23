import json

from sqlalchemy.orm import Session

from app.models.question_model import Question
from app.schemas.question_schema import QuestionCreate


def create_question(db: Session, question: QuestionCreate):
    question_data = question.dict()
    question_data["options"] = json.dumps(question.options)
    new_question = Question(**question_data)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()


def get_questions_by_quiz(db: Session, quiz_id: int):
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    for q in questions:
        q.options = json.loads(q.options)
    return questions


def delete_question(db: Session, question_id: int):
    question = get_question(db, question_id)
    if question:
        db.delete(question)
        db.commit()
    return question
