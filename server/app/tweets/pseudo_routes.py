from datetime import datetime, timezone
from typing import List

from fastapi import Depends
from pydantic import NonNegativeInt, PositiveInt, conint
from sqlmodel import Session, select

from app.auth.helper_functions import get_current_user
from app.auth.models import User
from app.config import settings
from app.database import get_or_404, get_session, save_and_refresh
from app.tweets.helper_functions import get_all_overview, get_db_overview

from . import router
from .models import Overview, PseudoTweet, Tweet, TweetUpdate


@router.get("/pseudo/overview", response_model=List[Overview])
def get_pseudo_overview(all: bool = False, session: Session = Depends(get_session)):
    """
    Get overview by grouping on created_at
    """

    if all:
        return get_all_overview(session)
    return get_db_overview(session, PseudoTweet)


@router.get("/pseudo", response_model=List[PseudoTweet])
def read_pseudo_tweets(
    offset: NonNegativeInt = 0,
    limit: conint(le=10, gt=0) = 10,
    minority: bool = False,
    session: Session = Depends(get_session),
):
    """
    Read pseudo tweets within the offset and limit
    """
    selection = select(PseudoTweet)
    if minority:
        # The lockdown has the lowest number of true examples for now
        selection = selection.filter(getattr(PseudoTweet, settings.minority_label))
    tweets = session.exec(selection.offset(offset).limit(limit)).all()
    return tweets


@router.get(
    "/pseudo/{pseudo_tweet_id}",
    response_model=PseudoTweet,
    responses={404: {"description": "PseudoTweet Not found"}},
)
def read_pseudo_tweet(
    pseudo_tweet_id: PositiveInt, session: Session = Depends(get_session)
):
    """
    Read a pseudo tweet by id.
    """
    tweet = get_or_404(session, PseudoTweet, pseudo_tweet_id)
    return tweet


@router.patch(
    "/pseudo/{pseudo_tweet_id}",
    response_model=Tweet,
    responses={404: {"description": "PseudoTweet Not found"}},
)
def verify_pseudo_tweet(
    pseudo_tweet_id: PositiveInt,
    tweet: TweetUpdate,
    db_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Verify a pseudo tweet by id.
    """

    db_pseudo_tweet = get_or_404(session, PseudoTweet, pseudo_tweet_id)

    # Exclude the nones
    tweet_data = tweet.dict(exclude_none=True)

    verified_tweet = Tweet.from_orm(
        db_pseudo_tweet,
        {
            **tweet_data,
            "id": None,  # Let database decide the id of the new row in Tweet
            "verified_at": datetime.now(timezone.utc),
            "verifier_id": db_user.id,  # Tweet needs the id when forming
        },
    )

    # Delete pseudo tweet
    session.delete(db_pseudo_tweet)

    # Save verified tweet and refresh it to get the new id
    save_and_refresh(session, verified_tweet)
    return verified_tweet
