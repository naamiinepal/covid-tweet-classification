from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, PositiveInt
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.auth.models import User

# Data Models


class Overview(BaseModel):
    covid_stats: int
    vaccination: int
    covid_politics: int
    humour: int
    lockdown: int
    civic_views: int
    life_during_pandemic: int
    covid_waves_and_variants: int
    others: int
    created_date: date


class TweetUpdate(BaseModel):
    covid_stats: Optional[bool] = None
    vaccination: Optional[bool] = None
    covid_politics: Optional[bool] = None
    humour: Optional[bool] = None
    lockdown: Optional[bool] = None
    civic_views: Optional[bool] = None
    life_during_pandemic: Optional[bool] = None
    covid_waves_and_variants: Optional[bool] = None


class TweetBase(SQLModel):
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


class TweetRead(TweetBase):
    others: bool


# Table Models


class Tweet(TweetBase, table=True):
    # The user who moved tweet from TweetBase to Tweet
    verifier_id: PositiveInt = Field(foreign_key="user.id")
    verifier: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Tweet.verifier_id"},
    )

    verified_at: datetime

    # The user who modified tweet in Tweet itself, so optional
    modifier_id: Optional[PositiveInt] = Field(default=None, foreign_key="user.id")
    modifier: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Tweet.modifier_id"},
    )

    modified_at: Optional[datetime] = Field(default=None)


class PseudoTweet(TweetBase, table=True):
    __tablename__ = "pseudo_tweet"
