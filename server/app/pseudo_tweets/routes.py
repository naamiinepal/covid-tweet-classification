from datetime import datetime, timezone
from typing import List, Optional

from fastapi import Depends
from pydantic import NonNegativeInt, PositiveInt, conint
from sqlmodel import Session

from ..auth.dependencies import get_current_user, get_username_from_token
from ..auth.models import User
from ..database import get_session, save_and_refresh
from ..tweets_common.helper_functions import (
    get_a_tweet,
    get_all_overview,
    get_combined_tweet,
    get_db_overview,
    get_scalar_select,
    make_tweet_read,
)
from ..tweets_common.models import (
    Overview,
    PseudoTweet,
    Topics,
    Tweet,
    TweetRead,
    TweetUpdate,
)
from . import router


# Keep it in the top to avoid clashing with pseudo_tweet_id
@router.get("/overview", response_model=List[Overview])
def get_pseudo_overview(all: bool = False, session: Session = Depends(get_session)):
    """
    Get overview by grouping on created_at
    """

    if all:
        return get_all_overview(session)
    return get_db_overview(session, PseudoTweet)


@router.get("/", response_model=List[TweetRead])
def read_pseudo_tweets(
    offset: NonNegativeInt = 0,
    limit: conint(le=10, gt=0) = 10,
    filter_topic: Optional[Topics] = None,
    session: Session = Depends(get_session),
):
    """
    Read pseudo tweets within the offset and limit
    """
    selection = get_scalar_select(PseudoTweet)
    if filter_topic is not None:
        # The lockdown has the lowest number of true examples for now
        selection = selection.filter(getattr(PseudoTweet, filter_topic))
    tweets = session.exec(selection.offset(offset).limit(limit)).all()
    return tweets


@router.get(
    "/{pseudo_tweet_id}",
    response_model=TweetRead,
    responses={404: {"description": "PseudoTweet Not found"}},
)
def read_pseudo_tweet(
    pseudo_tweet_id: PositiveInt, session: Session = Depends(get_session)
):
    """
    Read a pseudo tweet by id.
    """
    pseudo_tweet = get_a_tweet(session, pseudo_tweet_id, PseudoTweet)

    return pseudo_tweet


@router.patch(
    "/{pseudo_tweet_id}",
    response_model=TweetRead,
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

    db_pseudo_tweet, others = get_combined_tweet(session, pseudo_tweet_id, PseudoTweet)

    # Exclude the nones
    tweet_data = tweet.dict(exclude_none=True)

    verified_tweet = Tweet.from_orm(
        db_pseudo_tweet,
        {
            **tweet_data,
            "id": None,  # Let database decide the id of the new row in Tweet
            "verified_at": datetime.now(timezone.utc),
            "verifier_id": db_user.id,  # Tweet needs the user id when forming
        },
    )

    # Delete pseudo tweet
    session.delete(db_pseudo_tweet)

    # Save verified tweet and refresh it to get the new id
    save_and_refresh(session, verified_tweet)

    return make_tweet_read(db_pseudo_tweet, others)


@router.delete(
    "/{pseudo_tweet_id}",
    response_model=TweetRead,
    responses={404: {"description": "PseudoTweet Not found"}},
)
def delete_pseudo_tweet(
    pseudo_tweet_id: PositiveInt,
    _: User = Depends(get_username_from_token),
    session: Session = Depends(get_session),
):
    """
    Delete a pseudo tweet by id.
    """

    db_pseudo_tweet, others = get_combined_tweet(session, pseudo_tweet_id, PseudoTweet)

    session.delete(db_pseudo_tweet)
    session.commit()
    return make_tweet_read(db_pseudo_tweet, others)
