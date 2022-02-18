from datetime import date, datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, PositiveInt
from sqlmodel import Field, Relationship, SQLModel, func

if TYPE_CHECKING:
    from app.auth.models import User

# Data Models


class Topics(str, Enum):
    """
    Used as choices to filter the tweets
    """

    covid_stats = "covid_stats"
    vaccination = "vaccination"
    covid_politics = "covid_politics"
    humour = "humour"
    lockdown = "lockdown"
    civic_views = "civic_views"
    life_during_pandemic = "life_during_pandemic"
    covid_waves_and_variants = "covid_waves_and_variants"
    others = "others"


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
        back_populates="verified_tweets",
        sa_relationship_kwargs={"foreign_keys": "Tweet.verifier_id"},
    )

    # Do not manually modify it
    verified_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()},
    )

    # The user who modified tweet in Tweet itself, so optional
    modifier_id: Optional[PositiveInt] = Field(default=None, foreign_key="user.id")
    modifier: Optional["User"] = Relationship(
        back_populates="modified_tweets",
        sa_relationship_kwargs={"foreign_keys": "Tweet.modifier_id"},
    )

    modified_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"onupdate": func.now()}
    )


class PseudoTweet(TweetBase, table=True):
    __tablename__ = "pseudo_tweet"
