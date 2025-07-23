from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db_connection import get_db
from app.models import Course, Lesson
from app.models import question_model as Question
from app.models import quiz_model as Quiz

router = APIRouter()


@router.get("/dashboard-data")
def get_dashboard_data(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    data = []
    for course in courses:
        lessons = db.query(Lesson).filter_by(course_id=course.id).all()
        course_data = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "lessons": []
        }

        for lesson in lessons:
            quizzes = db.query(Quiz).filter_by(lesson_id=lesson.id).all()
            lesson_data = {
                "id": lesson.id,
                "title": lesson.title,
                "quizzes": []
            }

            for quiz in quizzes:
                questions = db.query(Question).filter_by(quiz_id=quiz.id).all()
                quiz_data = {
                    "id": quiz.id,
                    "title": quiz.title,
                    "questions": [{"id": q.id, "question": q.question} for q in questions]
                }

                lesson_data["quizzes"].append(quiz_data)

            course_data["lessons"].append(lesson_data)

        data.append(course_data)

    return {"courses": data}
