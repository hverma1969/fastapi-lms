from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal
from app.schemas import lesson as schemas

router = APIRouter(prefix="/lessons", tags=["Lessons"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.LessonOut)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(get_db)):
    db_lesson = models.lesson.Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@router.get("/{lesson_id}", response_model=schemas.LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(models.lesson.Lesson).filter(
        models.lesson.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson
