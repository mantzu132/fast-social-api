from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uuid
from typing import Optional


class Post(BaseModel):
    title: str
    content: str


app = FastAPI()
my_posts = []


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_data = post.dict()
    post_id = uuid.uuid4()
    post_data["id"] = post_id
    my_posts.append(post_data)
    return post_data


@app.get("/posts/{post_id}")
async def get_post(post_id: uuid.UUID) -> Post:
    for post in my_posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")
