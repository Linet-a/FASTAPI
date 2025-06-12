from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import get_db



router = APIRouter(
    prefix= "/users",
    tags = ["Users"]
    )

#usercreate router
@router.post("/", response_model=schemas.UserResponse, status_code = status.HTTP_201_CREATED)
def create_users(user:schemas.UserCreate, db:Session = Depends(get_db)):
    user_data = user.model_dump() #because.dict() is deprecated
    current_user = models.User(**user_data)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id:int, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the {user_id} not found")
    return user