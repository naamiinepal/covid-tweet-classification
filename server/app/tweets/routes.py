from typing import List

from pydantic import conint, NonNegativeInt, PositiveInt

from fastapi import Depends

from sqlmodel import Session, select

from app.database import get_session, get_or_404

from . import router
from .models import Tweet


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
