from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from . import router
from .helper_functions import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    oauth2_scheme,
)
from .models import Token, User


@router.get(
    "/items",
    responses={401: {"description": "User Not Authenticated"}},
)
async def get_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.get(
    "/me",
    response_model=User,
    responses={
        400: {"description": "Inactive User"},
        401: {"description": "Authentication Error"},
    },
)
async def get_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post(
    "/token",
    response_model=Token,
    responses={400: {"description": "Incorrect Username or Password"}},
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(400, "Incorrect Username or Password")

    access_token = await create_access_token({"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
