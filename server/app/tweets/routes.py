from typing import List

from pydantic import conint, NonNegativeInt, PositiveInt

from fastapi import Depends

from sqlmodel import Session, select, func, cast, Integer

from app.database import get_session, get_or_404

from . import router
from .models import Overview, Tweet


@router.get("/overview", response_model=List[Overview])
def get_overview(session: Session = Depends(get_session)):
    """
    Get overview by grouping on created_at
    """
    tweets = session.exec(
        select(
            func.sum(cast(Tweet.covid_stats, Integer)).label("covid_stats"),
            func.sum(cast(Tweet.vaccination, Integer)).label("vaccination"),
            func.sum(cast(Tweet.covid_politics, Integer)).label("covid_politics"),
            func.sum(cast(Tweet.humour, Integer)).label("humour"),
            func.sum(cast(Tweet.lockdown, Integer)).label("lockdown"),
            func.sum(cast(Tweet.civic_views, Integer)).label("civic_views"),
            func.sum(cast(Tweet.life_during_pandemic, Integer)).label(
                "life_during_pandemic"
            ),
            func.sum(cast(Tweet.covid_waves_and_variants, Integer)).label(
                "covid_waves_and_variants"
            ),
            func.sum(cast(Tweet.misinformation, Integer)).label("misinformation"),
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
