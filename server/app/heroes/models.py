from typing import Optional

from sqlmodel import Field, SQLModel

# Data Models


class HeroCreate(SQLModel):
    """
    Data Model for Hero Creation
    """

    name: str
    secret_name: str
    age: Optional[int] = None


class HeroRead(HeroCreate):
    """
    Data Model for Hero Read
    """

    id: int


class HeroUpdate(SQLModel):
    """
    Data Model for Hero Update
    """

    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


# Table Models


class Hero(HeroCreate, table=True):
    """
    Table Model for Hero
    """

    id: Optional[int] = Field(default=None, primary_key=True)
