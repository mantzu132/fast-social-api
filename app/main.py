from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uuid
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os

# Connect to the database
while True:
    try:
        conn = psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except psycopg2.OperationalError as e:
        print(f"Error: {e}. Retrying in 2 seconds...")
        time.sleep(2)


# Schema for api
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


app = FastAPI()

# ---------------------------------------------------------------- ENDPOINTS START HERE


# Gets all posts
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    records = cursor.fetchall()
    return {"data": records}


# Create a post and add it to the posts table
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_data = post.dict()
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post_data["title"], post_data["content"], post_data["published"]),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# Get a specific post by id from the posts table.
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    if record := cursor.fetchone():
        return {"data": record}
    raise HTTPException(status_code=404, detail="Post not found")


# Delete a post if we find one
@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int):
    cursor.execute(
        "DELETE FROM posts WHERE id = %s RETURNING *",
        (post_id,),
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post:
        return {"detail": "Post deleted", "data": deleted_post}
    raise HTTPException(status_code=404, detail="Post not found")


# Updates a post by searching for the post id in posts table.
@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post):
    updated_data = updated_post.dict()
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (
            updated_data["title"],
            updated_data["content"],
            updated_data["published"],
            post_id,
        ),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post:
        return {"data": updated_post}
    raise HTTPException(status_code=404, detail="Post not found")
