from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.db_connection import get_db
from app.models.lesson_progress import LessonProgress as Lesson
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_model import Quiz
from app.models.user import User

router = APIRouter()


@router.post("/lesson/{lesson_id}/complete")
def mark_lesson_completed(lesson_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    progress = db.query(LessonProgress).filter_by(
        user_id=user.id, lesson_id=lesson_id).first()
    if progress:
        progress.completed = True
    else:
        progress = LessonProgress(
            user_id=user.id, lesson_id=lesson_id, completed=True)
        db.add(progress)
    db.commit()
    return {"message": "Lesson marked as completed."}


router = APIRouter()


@router.post("/quiz/{quiz_id}/submit")
def submit_quiz(quiz_id: int, score: float, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attempt = QuizAttempt(user_id=user.id, quiz_id=quiz_id, score=score)
    db.add(attempt)
    db.commit()
    return {"message": "Quiz attempt recorded."}


@router.get("/course/{course_id}/progress")
def get_course_progress(course_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_lessons = db.query(Lesson).filter_by(course_id=course_id).count()
    completed_lessons = (
        db.query(LessonProgress)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .filter(Lesson.course_id == course_id, LessonProgress.user_id == user.id, LessonProgress.completed == True)
        .count()
    )

    quiz_scores = (
        db.query(QuizAttempt)
        .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
        .filter(Quiz.course_id == course_id, QuizAttempt.user_id == user.id)
        .all()
    )

    percent_complete = round(
        (completed_lessons / total_lessons) * 100, 2) if total_lessons else 0

    return {
        "lessons_completed": completed_lessons,
        "total_lessons": total_lessons,
        "course_completion": f"{percent_complete}%",
        "quiz_attempts": [{"quiz_id": q.quiz_id, "score": q.score, "timestamp": q.timestamp} for q in quiz_scores],
    }
