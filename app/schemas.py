from pydantic import BaseModel, EmailStr



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
