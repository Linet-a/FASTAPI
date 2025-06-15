from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import get_db, hash_password



router = APIRouter(
    prefix= "/users",
    tags = ["Users"]
    )

#usercreate route
@router.post("/", response_model=schemas.UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)

    current_user = models.User(email=user.email, hashed_password=hashed_pwd)# storre the hashed password

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user


#delete user



