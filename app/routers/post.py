from fastapi import Depends, HTTPException, status, APIRouter
from .. import model, schema, oauth2
from ..database import Session, get_db
from typing import Optional

# create a router object
router = APIRouter(prefix="/posts", tags=["Posts"])


# Get all posts


@router.get("/", response_model=list[schema.ReturnPost])
def get_all_posts(
    db: Session = Depends(get_db),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    title: Optional[str] = None,
):
    query = db.query(model.Post)

    if title:
        query = query.filter(model.Post.title.ilike(f"%{title}%"))

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    posts = query.all()
    return posts


# Create a post and add it to the posts table
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.ReturnPost)
def create_post(
    post: schema.PostBase,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    new_post = model.Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get a specific post by id from the posts table.
@router.get("/{post_id}", response_model=schema.ReturnPost)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).get(post_id)
    if post:
        return post
    raise HTTPException(status_code=404, detail="Post not found")


# Delete a post if we find one
@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    post = db.query(model.Post).get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}


# Updates a post by searching for the post id in posts table.
@router.put("/{post_id}", response_model=schema.ReturnPost)
def update_post(
    post_id: int,
    updated_post: schema.CreatePost,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    post = db.query(model.Post).filter(model.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    for key, value in updated_post.dict().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post
