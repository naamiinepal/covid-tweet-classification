from typing import Optional

from pydantic import BaseModel, PositiveInt
from sqlmodel import Field, SQLModel

# Data Models


class HeroCreate(SQLModel):
    """
    Data Model for Hero Creation
    """

    name: str
    secret_name: str
    age: Optional[PositiveInt] = None


class HeroRead(HeroCreate):
    """
    Data Model for Hero Read
    """

    id: PositiveInt


class HeroUpdate(BaseModel):
    """
    Data Model for Hero Update
    """

    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[PositiveInt] = None


# Table Models


class Hero(HeroCreate, table=True):
    """
    Table Model for Hero
    """

    id: Optional[PositiveInt] = Field(default=None, primary_key=True)
