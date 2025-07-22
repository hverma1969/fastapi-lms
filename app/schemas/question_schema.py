from pydantic import BaseModel, conint


class QuestionCreate(BaseModel):
    text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_option: conint(ge=1, le=4)  # Ensures value is between 1 and 4
    quiz_id: int


class Question(BaseModel):
    id: int
    text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_option: int
    quiz_id: int

    class Config:
        orm_mode = True
