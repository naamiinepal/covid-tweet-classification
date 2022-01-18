from datetime import datetime
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
