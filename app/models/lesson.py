from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    resource_links = Column(Text, nullable=True)

    course_id = Column(Integer, ForeignKey(
        "courses.id", ondelete="CASCADE"), nullable=False)

    course = relationship("Course", back_populates="lessons")
