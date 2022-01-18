from datetime import datetime, date
from typing import Optional

from pydantic import PositiveInt
from sqlmodel import Field, SQLModel

# Data Models


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
