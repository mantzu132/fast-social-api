from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from fastapi import Depends, HTTPException, status
from . import schema
from fastapi.security import OAuth2PasswordBearer
from .database import Session, get_db
from . import model
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_jwt_token(
    *,
    data: dict,
    secret_key: str = settings.SECRET_KEY,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # Validate the payload using the Pydantic model
        valid_payload = schema.JWTPayload(**payload)

        return valid_payload.user_id

    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_token(token, credentials_exception)
    user = db.query(model.User).filter(model.User.id == user_id).first()

    return user
