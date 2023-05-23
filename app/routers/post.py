from fastapi import Depends, HTTPException, status, APIRouter
from .. import model, schema, oauth2
from ..database import Session, get_db
from typing import Optional
from sqlalchemy import func

# create a router object
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schema.ReturnPostWithVotes])
def get_all_posts(
    db: Session = Depends(get_db),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    title: Optional[str] = None,
):
    # First query that gets all posts along with the count of votes for each post
    query = (
        db.query(model.Post, func.count(model.Votes.post_id).label("vote_count"))
        .outerjoin(model.Votes, model.Post.id == model.Votes.post_id)
        .group_by(model.Post.id)
    )

    # Query parameters to filter by title, limit amount of posts shown and offset (skip through) a number of posts.
    if title:
        query = query.filter(model.Post.title.ilike(f"%{title}%"))

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    posts = query.all()

    # Since the return from query is a list of tuples, we need to unpack the tuples and create a list of dictionaries
    return [{"post": post, "vote_count": vote_count} for post, vote_count in posts]


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


@router.get("/{post_id}", response_model=schema.ReturnPostWithVotes)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post_with_votes = (
        db.query(model.Post, func.count(model.Votes.post_id).label("vote_count"))
        .outerjoin(model.Votes, model.Post.id == model.Votes.post_id)
        .filter(model.Post.id == post_id)
        .group_by(model.Post.id)
        .first()
    )

    if post_with_votes:
        post, vote_count = post_with_votes
        return {"post": post, "vote_count": vote_count}

    raise HTTPException(status_code=404, detail="Post not found")


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
