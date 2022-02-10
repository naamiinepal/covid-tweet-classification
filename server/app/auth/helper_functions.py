from datetime import datetime, timedelta, timezone
from typing import Any, AnyStr, Mapping, Optional

import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.config import settings

from .models import Token, User

# Password context
pwd_context = CryptContext(schemes=["argon2"])


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
    user = session.exec(select(User).where(User.username == username)).one_or_none()
    return user


def create_access_token(
    to_encode: Mapping[str, Any],
    expires_delta: Optional[timedelta] = None,
):
    """
    Create an access token
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(
        {**to_encode, "exp": expire},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def create_access_token_from_username(
    username: str,
    expires_delta: Optional[timedelta] = None,
):
    """
    Create an access token from a username.
    This is a more specific version of `create_access_token`.
    """
    token = create_access_token({"sub": username}, expires_delta)
    return Token(access_token=token)


def authenticate_user(session: Session, username: str, plain_password: str):
    """
    Authenticate a user
    """
    user = get_user(session, username)
    if user is not None and verify_password(plain_password, user.hashed_password):
        return user
