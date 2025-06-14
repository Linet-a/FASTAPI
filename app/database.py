from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Engine : PostgreSQL
DATABASE_URL = "postgresql://postgres:linet123@localhost:5432/fastapi"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
