from fastapi import Depends, HTTPException, status, APIRouter
from .. import model, schema, utils
from ..database import Session, get_db


# create a router object
router = APIRouter(prefix="/users", tags=["Users"])


# add an user to the table of users
@router.post("/", response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    new_user = model.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get user by id from the table of users
@router.get("/{user_id}", response_model=schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).get(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
