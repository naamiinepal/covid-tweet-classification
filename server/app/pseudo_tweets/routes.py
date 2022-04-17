from datetime import date
from typing import List, Optional

from fastapi import Depends, Query
from pydantic import NonNegativeInt, PositiveInt, conint
from sqlmodel import Session

from ..auth.dependencies import get_current_user, get_username_from_token
from ..auth.models import User
from ..database import get_session, save_and_refresh
from ..tweets_common.helper_functions import (
    get_a_tweet,
    get_combined_model,
    get_combined_tweet,
    get_db_overview,
    get_filtered_count,
    get_filtered_selection,
    make_tweet_read,
)
from ..tweets_common.models import (
    Overview,
    PseudoTweet,
    Topics,
    Tweet,
    TweetCount,
    TweetRead,
    TweetUpdate,
)
from ..tweets_common.types import Month
from . import router


# Keep it in the top to avoid clashing with pseudo_tweet_id
@router.get("/overview", response_model=List[Overview])
def get_pseudo_overview(all: bool = False, session: Session = Depends(get_session)):
    """
    Get overview by grouping on created_at
    """

    Model = get_combined_model() if all else PseudoTweet

    return get_db_overview(session, Model)


@router.get("/count", response_model=TweetCount)
def get_count(
    topics: Optional[List[Topics]] = Query(None),
    day: Optional[date] = None,
    month: Optional[Month] = None,
    all: bool = False,
    session: Session = Depends(get_session),
):
    """
    Get the count of pseudo tweets for the given filters
    """

    Model = get_combined_model() if all else PseudoTweet

    return get_filtered_count(Model, topics, day, month, session)


@router.get("/", response_model=List[TweetRead])
def read_pseudo_tweets(
    offset: NonNegativeInt = 0,
    limit: conint(le=10, gt=0) = 10,
    topics: Optional[List[Topics]] = Query(None),
    day: Optional[date] = None,
    month: Optional[Month] = Query(None, description="Month in %Y-%m format"),
    maximize_labels: bool = False,
    session: Session = Depends(get_session),
):
    """
    Read pseudo tweets within the offset and limit
    """
    selection = get_filtered_selection(topics, PseudoTweet, day, month)

    # others should be exclusively provided, hence the last check
    is_others = topics is not None and len(topics) and topics[0] == Topics.others

    # No need to maximize labels if sorted by others
    if maximize_labels and not is_others:

        def get_model_attr(attr: str):
            """Get attr of PseudoTweet"""
            return getattr(PseudoTweet, attr)

        first, *rest = tuple(map(get_model_attr, TweetUpdate.__fields__))
        selection = selection.order_by(sum(rest, first).desc())
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
            "verifier_id": db_user.id,  # Tweet needs the user id when forming
        },
    )

    # Delete pseudo tweet
    session.delete(db_pseudo_tweet)

    # Save verified tweet and refresh it to get the new id
    save_and_refresh(session, verified_tweet)

    return make_tweet_read(verified_tweet, others)


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


@router.post("/edit_request/{pseudo_tweet_id}")
def request_pseudo_tweet_edit(pseudo_tweet_id: PositiveInt, tweet: TweetUpdate):
    """
    Request for pseudo tweet edit
    """
    # NOTE: DANGER...CHANGE THIS CODE
    # ONLY FOR DEMO PURPOSE
    with open("edits.txt", "a", encoding="utf-8") as f:
        f.write(f"Pseudo Tweet, {pseudo_tweet_id}, {tweet}\n")

    return {"message": "Successfully submitted edit request."}
