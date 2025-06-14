from .database import SessionLocal
from passlib.context import CryptContext



#provide a dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#define a a function that hashes user pasword
def hash_password(user_pswd:str) -> str:
    return pwd_context.hash(user_pswd)
   


#define a function that verifies user pasword aginst the hashed password

def verify_password(plain_password:str, hashed_password:str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

