from .database import Session
from .model import Post
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
import uuid
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os


# SQLAHLCHMY STUFF
session = Session()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# ----------------


# Schema for fastapi
class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True


app = FastAPI()

# ---------------------------------------------------------------- ENDPOINTS START HERE


# Gets all posts
@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


# Create a post and add it to the posts table
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostSchema, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


# Get a specific post by id from the posts table.
@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if post:
        return {"data": post}
    raise HTTPException(status_code=404, detail="Post not found")


# Delete a post if we find one
@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if post:
        db.delete(post)
        db.commit()
        return {"detail": "Post deleted", "data": post}
    raise HTTPException(status_code=404, detail="Post not found")


# Updates a post by searching for the post id in posts table.
@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: PostSchema, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if post:
        for key, value in updated_post.dict().items():
            setattr(post, key, value)
        db.commit()
        db.refresh(post)
        return {"data": post}
    raise HTTPException(status_code=404, detail="Post not found")
