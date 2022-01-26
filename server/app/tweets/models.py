from datetime import date, datetime
from typing import Optional

from pydantic import PositiveInt
from sqlmodel import Field, Relationship, SQLModel

from app.auth.models import User

# Data Models


class Overview(SQLModel):
    covid_stats: int
    vaccination: int
    covid_politics: int
    humour: int
    lockdown: int
    civic_views: int
    life_during_pandemic: int
    covid_waves_and_variants: int
    misinformation: int
    created_at: date


class TweetUpdate(SQLModel):
    text: Optional[str] = None
    covid_stats: Optional[bool] = None
    vaccination: Optional[bool] = None
    covid_politics: Optional[bool] = None
    humour: Optional[bool] = None
    lockdown: Optional[bool] = None
    civic_views: Optional[bool] = None
    life_during_pandemic: Optional[bool] = None
    covid_waves_and_variants: Optional[bool] = None
    misinformation: Optional[bool] = None


# Table Models


class Tweet(SQLModel, table=True):
    id: Optional[PositiveInt] = Field(default=None, primary_key=True)
    text: str
    username: str
    created_at: datetime
    covid_stats: bool
    vaccination: bool
    covid_politics: bool
    humour: bool
    lockdown: bool
    civic_views: bool
    life_during_pandemic: bool
    covid_waves_and_variants: bool
    misinformation: bool

    modifier_id: Optional[PositiveInt] = Field(default=None, foreign_key="user.id")
    modifier: Optional[User] = Relationship(back_populates="tweets")

    modified_at: Optional[datetime] = Field(default=None)
