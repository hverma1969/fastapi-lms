from typing import List

from pydantic import BaseModel


class QuestionCreate(BaseModel):
    text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_option: int


# schemas/quiz.py

class QuizCreate(BaseModel):
    title: str
    course_id: int
    questions: List[QuestionCreate]
