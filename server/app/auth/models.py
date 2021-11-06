from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


# Data Models


class Token(BaseModel):
    """
    Token response model
    """

    access_token: str
    token_type: str = "bearer"


class UserBase(SQLModel):
    """
    Base user model
    """

    username: str
    email: Optional[str] = None
    full_name: str


class UserCreate(UserBase):
    """
    User create model
    """

    password: str


class UserRead(UserBase):
    """
    User read model
    """

    id: int


class UserUpdate(SQLModel):
    """
    User update model
    """

    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


# Table Models


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
