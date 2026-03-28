from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ---------------- USER ----------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# ---------------- POST ----------------

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: Optional[int]
    user: Optional[UserResponse]

    class Config:
        from_attributes = True


# ---------------- FINAL OUTPUT ----------------

class PostOut(BaseModel):
    Post: PostResponse
    likes: int

    class Config:
        from_attributes = True