from datetime import datetime, timedelta, timezone
from typing import Any, AnyStr, Mapping, Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.database import get_session

from .models import Token, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Password context
pwd_context = CryptContext(schemes=["argon2"])

# JWT Config
JWT_SECRET_KEY = "EKKxDOzlMWZhZFQCQBCBDLY9RKVRctQucr5r"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: AnyStr, hashed_password: AnyStr) -> bool:
    """
    Check if the `hashed_password` is the hased version of `plain_password`
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: AnyStr) -> str:
    """
    Hash a plain text password
    """
    return pwd_context.hash(plain_password)


def get_user(session: Session, username: str):
    """
    Get a user from the DB
    """
    user = session.exec(select(User).where(User.username == username)).first()
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    """
    Get the current user from the JWT token
    """
    credentials_exception = HTTPException(
        401,
        detail="Invalid Authentication Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        raise credentials_exception
    else:
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception

    user = get_user(session, username)

    if user is None:
        raise credentials_exception

    return user


def create_access_token(
    to_encode: Mapping[str, Any],
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    """
    Create an access token
    """
    expire = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(
        {**to_encode, "exp": expire}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


def create_access_token_from_username(username: str, *args, **kwargs):
    """
    Create an access token from a username.
    This is a more specific version of `create_access_token`.
    """
    token = create_access_token({"sub": username}, *args, **kwargs)
    return Token(access_token=token)


def authenticate_user(session: Session, username: str, plain_password: str):
    """
    Authenticate a user
    """
    user = get_user(session, username)
    if user is not None and verify_password(plain_password, user.hashed_password):
        return user
