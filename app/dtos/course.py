from datetime import datetime

from pydantic import BaseModel, condecimal


class CourseCreate(BaseModel):
    title: str
    description: str | None = None
    instructor: str
    price: condecimal(max_digits=10, decimal_places=2)


class CourseOut(CourseCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
