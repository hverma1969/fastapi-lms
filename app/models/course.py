from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    instructor = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)  # <- Added

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    lessons = relationship("Lesson", back_populates="course",
                           cascade="all, delete")
    quizzes = relationship(
        "Quiz", back_populates="course", cascade="all, delete")
