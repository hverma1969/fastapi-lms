from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer

from app.db_connection import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
