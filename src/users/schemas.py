from typing import Sequence

from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    name: str
    surname_1: str
    surname_2: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResult(UserBase):
    pass


class UserList(BaseModel):
    results: Sequence[UserResult]
