from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..utils import get_db, verify_password

router = APIRouter(

    tags=["Authentication"]
)

#user login route
@router.post("/login")
def log_user(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    """
        check if user is in the database
        very if their passwords match: 
        provide an access token
        return sucess message
    """
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not db_user or  not verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")
    
    access_token = oauth2.create_token(data={"user_id":db_user.id})

    return {"access_token": access_token, "token_type":"bearer"}