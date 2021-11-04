from typing import Optional

from sqlmodel import Field, SQLModel

# Data Models


class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None


class HeroRead(HeroCreate):
    id: int


# Table Models


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


class Hero(HeroCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
