from typing import List, Optional

from pydantic import BaseModel


class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None


class QuizCreate(QuizBase):
    course_id: int


class QuizOut(QuizBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True  # use this instead of 'orm_mode' in Pydantic v2
