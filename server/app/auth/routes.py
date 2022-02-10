from typing import List

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, or_, select

from ..database import get_session, save_and_refresh
from . import router
from .dependencies import get_current_user, get_username_from_token
from .helper_functions import (
    authenticate_user,
    create_access_token_from_username,
    get_password_hash,
)
from .models import Token, User, UserCreate, UserRead, UserUpdate


@router.get(
    "/me",
    response_model=UserRead,
    responses={401: {"description": "Authentication Error"}},
)
async def get_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user
    """
    return current_user


@router.post(
    "/login",
    response_model=Token,
    responses={400: {"description": "Incorrect Username or Password"}},
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    Login user and return access token
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(400, "Incorrect Username or Password")

    return create_access_token_from_username(user.username)


# TODO: Store verifier somewhere
@router.post(
    "/register",
    response_model=Token,
    responses={400: {"description": "The Username Already Exists"}},
)
def register(
    user: UserCreate,
    _: User = Depends(
        get_username_from_token
    ),  # Avoid accessing the database since it is not used anywhere
    session: Session = Depends(get_session),
):
    """
    Register user and return access token
    """
    prev_users: List[User] = session.exec(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    ).all()
    if prev_users:
        username_match = False
        email_match = False
        # I have not kept break and checks since max(len(db_users)) = 2
        for u in prev_users:
            if u.username == user.username:
                username_match = True
            if u.email == user.email:
                email_match = True
        if username_match and email_match:
            detail = f"username: {user.username} and the email: {user.email}"
        elif username_match:
            detail = f"username: {user.username}"
        else:
            detail = f"email: {user.email}"
        raise HTTPException(status_code=400, detail=f"The {detail} already exists.")

    hashed_password = get_password_hash(user.password)
    db_user = User.from_orm(user, {"hashed_password": hashed_password})

    # Save user to database but now db_user has expired and doesn't contain anything
    save_and_refresh(session, db_user, refresh=False)

    return create_access_token_from_username(user.username)


@router.patch(
    "/update",
    response_model=UserRead,
    responses={
        401: {"description": "Authentication Error"},
        400: {"description": "No Valid Data to Update"},
    },
)
def update(
    user: UserUpdate,
    db_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update current user
    """

    # Exclude the nones
    user_dict = user.dict(exclude_none=True)

    if len(user_dict) == 0:
        raise HTTPException(status_code=400, detail="No Valid Data to Update")

    for key, value in user_dict.items():
        if key == "password":
            hashed_password = get_password_hash(value)
            db_user.hashed_password = hashed_password
        else:
            setattr(db_user, key, value)

    save_and_refresh(session, db_user)

    return db_user
