from .database import Session
from . import model, schema, utils
from fastapi import Depends, FastAPI, HTTPException, status


# SQLAHLCHMY STUFF
session = Session()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# ----------------


app = FastAPI()

# ---------------------------------------------------------------- POST PATHS START HERE


# Get all posts
@app.get("/posts", response_model=list[schema.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts


# Create a post and add it to the posts table
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostBase, db: Session = Depends(get_db)):
    new_user = model.Post(**post.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get a specific post by id from the posts table.
@app.get("/posts/{post_id}", response_model=schema.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).get(post_id)
    if post:
        return post
    raise HTTPException(status_code=404, detail="Post not found")


# Delete a post if we find one
@app.delete(
    "/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schema.Post
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).get(post_id)
    if post:
        db.delete(post)
        db.commit()
        return {"detail": "Post deleted", "data": post}
    raise HTTPException(status_code=404, detail="Post not found")


# Updates a post by searching for the post id in posts table.
@app.put("/posts/{post_id}", response_model=schema.Post)
def update_post(
    post_id: int, updated_post: schema.CreatePost, db: Session = Depends(get_db)
):
    post = db.query(model.Post).get(post_id)
    if post:
        for key, value in updated_post.dict().items():
            setattr(post, key, value)
        db.commit()
        db.refresh(post)
        return post
    raise HTTPException(status_code=404, detail="Post not found")


# -------------- user
@app.post("/users", response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    new_user = model.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
