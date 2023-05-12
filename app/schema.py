# Schema for fastapi
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class Post(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    # Providing an example for my schema
    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "secure_password",
            }
        }


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
