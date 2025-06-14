from pydantic import BaseModel, EmailStr
from typing import Optional



class PostBase(BaseModel):
    title: str
    content: str

#class PostCreate(PostBase):
    #published:bool = True

class PostResponse(PostBase):
    id: int

    class Config:
        orm_mode = True


       
#users schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


#user login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None