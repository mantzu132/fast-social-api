# Schema for fastapi
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


# Schema for the response of returning a user
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# Schema for our response of returning a post
class ReturnPost(PostBase):
    created_at: datetime
    user: UserOut

    class Config:
        orm_mode = True


class ReturnPostWithVotes(BaseModel):
    post: ReturnPost
    vote_count: int


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


# Schema for the user providing us the token
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for our token data (the data that we embedded into the token) TokenData
class JWTPayload(BaseModel):
    user_id: Optional[int] = None


# Schema for upvoting a post
# if dir 1 = upvote, if dir = 0 = remove the upvote
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
