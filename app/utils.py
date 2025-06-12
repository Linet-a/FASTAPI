from .database import SessionLocal


#provide a dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()