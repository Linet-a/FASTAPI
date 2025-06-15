from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


aoth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# a function for creating an access tocken
def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# a function to verify token
def verify_token(token:schemas.Token, credentials_exception):
    """
    takes in the token provided by the user
    decodes it and extracts the id -> or any other information passed in the payload
    verifies the id-> if correct return token data
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

 #getcur user   
def get_current_user(token:str = Depends(aoth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate detail",
                                          headers={"www-Authenticate": "Bearer"})
    return verify_token(token, credentials_exception )
