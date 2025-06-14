from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..utils import get_db
from . import  auth
#from sqlalchemy import List





router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)

#create post router

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.PostBase, db:Session = Depends(get_db), user_id:int=
                Depends(oauth2.get_current_user)):
    post_data = post.model_dump() #because.dict() is deprecated

    print(user_id)

    new_post = models.Post(**post_data)

    #add crreated data to the database

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#retrieve one post                                                                                             
@router.get("/")
def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "No post has been found")
    return posts




#retrieve all posts
@router.get("/{post_id}", response_model = schemas.PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail= "Post with the id not found")
    
    return post

#update a post

@router.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: schemas.PostBase, db:Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = updated_post.title
    post.content = updated_post.content
    db.commit()
    db.refresh(post)

    return post

#delete a post
@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return

