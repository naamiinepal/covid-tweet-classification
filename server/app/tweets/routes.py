from typing import List, Optional

from fastapi import Depends, HTTPException
from pydantic import NonNegativeInt, PositiveInt, conint
from sqlmodel import Session

from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..database import get_session, save_and_refresh
from ..tweets_common.helper_functions import (
    get_a_tweet,
    get_combined_tweet,
    get_db_overview,
    get_filtered_selection,
    make_tweet_read,
)
from ..tweets_common.models import Overview, Topics, Tweet, TweetRead, TweetUpdate
from . import router


# Keep it in the top to avoid clashing with pseudo_tweet_id
@router.get("/overview", response_model=List[Overview])
def get_tweet_overview(session: Session = Depends(get_session)):
    """
    Get overview by grouping on created_at
    """

    return get_db_overview(session, Tweet)


@router.get("/", response_model=List[TweetRead])
def read_tweets(
    offset: NonNegativeInt = 0,
    limit: conint(le=10, gt=0) = 10,
    filter_topic: Optional[Topics] = None,
    session: Session = Depends(get_session),
):
    """
    Read tweets within the offset and limit
    """
    selection = get_filtered_selection(filter_topic, Tweet)

    tweets = session.exec(
        selection.order_by(Tweet.id.desc()).offset(offset).limit(limit)
    ).all()

    return tweets


@router.get(
    "/{tweet_id}",
    response_model=TweetRead,
    responses={404: {"description": "Tweet Not found"}},
)
def read_tweet(tweet_id: PositiveInt, session: Session = Depends(get_session)):
    """
    Read a tweet by id.
    """

    tweet = get_a_tweet(session, tweet_id, Tweet)

    return tweet


@router.patch(
    "/{tweet_id}",
    response_model=TweetRead,
    responses={
        404: {"description": "Tweet Not found"},
        400: {"description": "No Valid Data to Update"},
    },
)
def update_tweet(
    tweet_id: PositiveInt,
    tweet: TweetUpdate,
    db_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update a tweet by id.
    """

    # Exclude the nones
    tweet_data = tweet.dict(exclude_none=True)

    if len(tweet_data) == 0:
        raise HTTPException(status_code=400, detail="No Valid Data to Update")

    db_tweet, others = get_combined_tweet(session, tweet_id, Tweet)

    for key, value in tweet_data.items():
        setattr(db_tweet, key, value)

    db_tweet.modifier = db_user

    save_and_refresh(session, db_tweet)
    return make_tweet_read(db_tweet, others)
