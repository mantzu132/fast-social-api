from fastapi import Depends, HTTPException, status, APIRouter
from .. import model, schema, oauth2
from ..database import Session, get_db


# create a router object
router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/")
def upvote_post(
    vote: schema.Vote,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    post_exists = db.query(model.Post).filter_by(id=vote.post_id).first()

    if not post_exists:
        raise HTTPException(status_code=404, detail="Post does not exist.")

    existing_vote = (
        db.query(model.Votes)
        .filter_by(user_id=current_user.id, post_id=vote.post_id)
        .first()
    )

    if vote.dir == 1:
        if not existing_vote:
            new_vote = model.Votes(user_id=current_user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Vote already exists.")
    elif existing_vote:
        db.delete(existing_vote)
        db.commit()
    else:
        raise HTTPException(
            status_code=400, detail="Vote does not exist to be deleted."
        )

    return {"status": "success"}
