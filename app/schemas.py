from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class CreatePost(PostBase):
    pass
 

class Post(PostBase):
    id:int 
    created_at:datetime
    owner_id: int

    class Config:
      orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
      orm_mode = True

#class PostOut(PostBase):
    #Post: Post 
    #Votes: int

    #class Config:
      #orm_mode = True
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr 
    created_at:datetime  

class Token(BaseModel):
    acess_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)       