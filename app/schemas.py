from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class PostBase(BaseModel):
    title: str
    content: str

#class PostCreate(PostBase):
    #published:bool = True
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserResponse

    class Config:
        orm_mode = True

       
#users schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str



#user login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: int