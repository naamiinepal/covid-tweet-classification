from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt, constr
from sqlmodel import Field, SQLModel

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

    username: constr(
        strip_whitespace=True, to_lower=True, min_length=4, max_length=20
    ) = Field(index=True)
    email: Optional[EmailStr] = None
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

    id: PositiveInt


class UserUpdate(SQLModel):
    """
    User update model
    """

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


# Table Models


class User(UserBase, table=True):
    id: Optional[PositiveInt] = Field(default=None, primary_key=True)
    hashed_password: str
