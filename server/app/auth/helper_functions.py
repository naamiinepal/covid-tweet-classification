from datetime import datetime, timedelta, timezone
from typing import Any, AnyStr, Mapping, Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .models import User, UserInDB, fake_users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["argon2"])

JWT_SECRET_KEY = "EKKxDOzlMWZhZFQCQBCBDLY9RKVRctQucr5r"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_password(plain_password: AnyStr, hashed_password: AnyStr) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(plain_password: AnyStr) -> str:
    return pwd_context.hash(plain_password)


async def get_user(username: str):
    user_dict = fake_users_db.get(username)
    if user_dict is not None:
        return UserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
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

    user = await get_user(username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(400, "Inactive User")
    return current_user


async def create_access_token(
    to_encode: Mapping[str, Any],
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    expire = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(
        {**to_encode, "exp": expire}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(username: str, plain_password: str):
    user = await get_user(username)
    if user is not None and await verify_password(plain_password, user.hashed_password):
        return user
