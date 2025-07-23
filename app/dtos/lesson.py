from typing import Optional

from pydantic import BaseModel


class LessonBase(BaseModel):
    title: str
    video_url: str
    resource_links: Optional[str] = None


class LessonCreate(LessonBase):
    course_id: int


class LessonOut(LessonBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True
