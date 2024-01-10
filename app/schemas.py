from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from typing_extensions import Annotated


class UserBase(BaseModel):
    email: EmailStr


class UserRequest(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_model = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostRequest(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user: UserResponse

    class Config:
        orm_model = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(strict=True, ge=0, le=1)]

class VotedPost(BaseModel):
    Post: PostResponse
    votes: int