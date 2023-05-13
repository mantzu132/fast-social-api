from fastapi import Depends, HTTPException, status, APIRouter
from .. import model, schema, utils
from ..database import Session, get_db
from ..oauth2 import create_jwt_token


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")

    if not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    # create a access token
    access_token = create_jwt_token(data={"user_id": db_user.id})

    return {"access_token": access_token, "token_type": "bearer"}
