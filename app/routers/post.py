from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..utils import get_db
from . import  auth
from typing import List
#from sqlalchemy import List


router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)

#create post route
@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostBase,db: Session = Depends(get_db), 
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Create a new post
    """
    user_id = current_user.id

    # Add user ownership if your Post model has an owner_id column
    new_post = models.Post(owner_id = user_id, **post.dict())

    # Add and commit to database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



#get all posts 
@router.get("/", response_model = List[schemas.PostResponse], status_code=status.HTTP_200_OK)
def get_posts(db:Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(status_code=404, detail= "No post in the database")
    
    return posts

#retrieve one posts
@router.get("/{post_id}", response_model = schemas.PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail= "Post with the id not found")
    
    return post


#Get user specific posts
@router.get("/my_posts", response_model = List[schemas.PostResponse], status_code=status.HTTP_200_OK)
def get_posts(db:Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).filter(models.Post.id == current_user.id).all()

    if not posts:
        raise HTTPException(status_code=404, detail= "No post in the database")
    
    return posts

#get users's one post
@router.get("/my_post/{post_id}", response_model = schemas.PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db:Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).first()

    if not post:
        raise HTTPException(status_code=404, detail= "Post with the id not found")
    
    return post




#retrieve one posts
@router.get("/{post_id}", response_model = schemas.PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail= "Post with the id not found")
    
    return post

#update a post

@router.put("/{post_id}")
def update_post(post_id: int, updated_post: schemas.PostBase, db:Session= Depends(get_db), current_user:int=
                Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    post.title = updated_post.title
    post.content = updated_post.content
    db.commit()
    db.refresh(post)

    return post



# Delete a post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    print(post_query)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    post_query.delete(synchronize_session=False)  # Fast, but skips syncing session
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#pm.environment.set("JWT", pm.response.json().access_token);
