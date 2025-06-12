from fastapi import FastAPI
from .database import Base, engine
from . import models
from app.routers import users, post  # import the routers



app = FastAPI()


Base.metadata.create_all(bind=engine)


# include the routers
#app.include_router(users.router)
app.include_router(post.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}