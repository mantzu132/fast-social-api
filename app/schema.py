# Schema for fastapi
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


# Schema for our response of returning a post
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


# Schema for the response of returning a user
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# Schema for the user providing us the token
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for our token data (the data that we embedded into the token) TokenData
class JWTPayload(BaseModel):
    id: Optional[str] = None
