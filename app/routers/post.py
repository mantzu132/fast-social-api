from fastapi import Depends, HTTPException, status, APIRouter
from .. import model, schema, oauth2
from ..database import Session, get_db

# create a router object
router = APIRouter(prefix="/posts", tags=["Posts"])


# Get all posts
@router.get("/", response_model=list[schema.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts


# Create a post and add it to the posts table
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(
    post: schema.PostBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get a specific post by id from the posts table.
@router.get("/{post_id}", response_model=schema.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).get(post_id)
    if post:
        return post
    raise HTTPException(status_code=404, detail="Post not found")


# Delete a post if we find one
@router.delete("/{post_id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(model.Post).get(post_id)
    if post:
        db.delete(post)
        db.commit()
        return {"detail": "Post deleted", "data": post}
    raise HTTPException(status_code=404, detail="Post not found")


# Updates a post by searching for the post id in posts table.
@router.put("/{post_id}", response_model=schema.Post)
def update_post(
    post_id: int,
    updated_post: schema.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(model.Post).get(post_id)
    if post:
        for key, value in updated_post.dict().items():
            setattr(post, key, value)
        db.commit()
        db.refresh(post)
        return post
    raise HTTPException(status_code=404, detail="Post not found")
