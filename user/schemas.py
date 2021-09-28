from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    surname_1: str
    surname_2: str
    password: str


class ExtraInfoCreate(BaseModel):
    text: str
    completed: bool


class TODOUpdate(ExtraInfoCreate):
    id: int
