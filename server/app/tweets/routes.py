from typing import List

from fastapi import Depends
from pydantic import NonNegativeInt, PositiveInt, conint
from sqlmodel import Integer, Session, cast, func, select

from app.database import get_or_404, get_session

from . import router
from .models import Overview, Tweet


@router.get("/overview", response_model=List[Overview])
def get_overview(session: Session = Depends(get_session)):
    """
    Get overview by grouping on created_at
    """

    def get_overview_row(column: str):
        return func.sum(cast(getattr(Tweet, column), Integer)).label(column)

    tweets = session.exec(
        select(
            get_overview_row("covid_stats"),
            get_overview_row("vaccination"),
            get_overview_row("covid_politics"),
            get_overview_row("humour"),
            get_overview_row("lockdown"),
            get_overview_row("civic_views"),
            get_overview_row("life_during_pandemic"),
            get_overview_row("covid_waves_and_variants"),
            get_overview_row("misinformation"),
            Tweet.created_at,
        ).group_by(func.strftime("%Y-%m-%d", Tweet.created_at))
    ).all()
    return tweets


@router.get("/", response_model=List[Tweet])
def read_tweets(
    offset: NonNegativeInt = 0,
    limit: conint(le=10, gt=0) = 10,
    session: Session = Depends(get_session),
):
    """
    Read tweets within the offset and limit
    """
    tweets = session.exec(select(Tweet).offset(offset).limit(limit)).all()
    return tweets


@router.get(
    "/{tweet_id}",
    response_model=Tweet,
    responses={404: {"description": "Tweet Not found"}},
)
def read_tweet(tweet_id: PositiveInt, session: Session = Depends(get_session)):
    """
    Read a tweet by id.
    """
    tweet = get_or_404(session, Tweet, tweet_id)
    return tweet
