from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):  # to start program we use: uvicorn app.main:app
    title: str
    content: str
    published: bool = True  # if nothing is specified from postman body then defaulted to True
    # id : int


class PostCreate(PostBase):  # already has contents of its parent class by default
    pass  # request part


class UserCreate(BaseModel):  # request part
    email: EmailStr
    password: str


class UserOut(BaseModel):  # response part
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    # class Config:
    #     orm_mode = True


class PostResponse(PostBase):  # response part
    id: int
    title: str
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    # Post : dict
    # Votes : Optional[int]=0
    no_of_votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):  # check whether id is embedded into token string
    id: Optional[str] = None  # for now optional


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)