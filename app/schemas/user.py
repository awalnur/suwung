from pydantic import BaseModel, EmailStr
from pydantic.v1 import Field


class RegisterUser(BaseModel):
    username: str = Field(min_length=5, max_length=20, example="username")
    email: EmailStr = Field(example="email@example.com")
    password: str = Field(min_length=8, max_length=16, example="password")

    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    username: str = Field(min_length=5, max_length=20, example="username")
    password: str = Field(min_length=8, max_length=16, example="password")

    class Config:
        orm_mode = True

    # Compare this snippet from app/models/user.py:
