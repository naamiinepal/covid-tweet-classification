from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from ..config import settings
from ..database import get_session
from .helper_functions import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


credentials_exception = HTTPException(
    401,
    detail="Invalid Authentication Credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_username_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
    else:
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception

    return username


def get_current_user(
    session: Session = Depends(get_session),
    username: str = Depends(get_username_from_token),
):
    """
    Get the current user from the JWT token
    """

    user = get_user(session, username)

    if user is None:
        raise credentials_exception

    return user
