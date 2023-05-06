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
    post_data["id"] = uuid.uuid4()
    my_posts.append(post_data)
    return post_data


@app.get("/posts/{post_id}")
async def get_post(post_id: uuid.UUID) -> Post:
    for post in my_posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: uuid.UUID):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            del my_posts[index]
            return {"detail": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")


@app.put("/posts/{post_id}")
async def update_post(post_id: uuid.UUID, updated_post: Post):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            updated_data = updated_post.dict()
            updated_data["id"] = post_id
            my_posts[index] = updated_data
            return updated_data
    raise HTTPException(status_code=404, detail="Post not found")
