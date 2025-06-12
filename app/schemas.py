from pydantic import BaseModel, EmailStr



class PostBase(BaseModel):
    title: str
    content: str

#class PostCreate(PostBase):
    #published:bool = True

class PostResponse(PostBase):
    id: int

    class Config:
        orm_model = True




        


class UserCreate(BaseModel):
    username: str
    email: EmailStr
 
class UserResponse(UserCreate):
    #should return : id, email
    id: int

    class Config:
        orm_model = True