from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import get_db, hash_password, verify_password



router = APIRouter(
    prefix= "/users",
    tags = ["Users"]
    )

#usercreate router
@router.post("/", response_model=schemas.UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)

    current_user = models.User(email=user.email, hashed_password=hashed_pwd)# storre the hashed password

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user

#user login route
@router.post("/login")
def log_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    """
        check if user is in the database
        very if their apsswords match: 
        return sucess message
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or  not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")
    return {"message":"user successfullly logged in"}



