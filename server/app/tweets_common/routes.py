from datetime import date
from typing import Optional, Tuple

from fastapi import Depends, Query
from sqlmodel import Session, select, union_all

from app.tweets_common.decorators import timed_lru_cache
from app.tweets_common.helper_functions import get_filtered_selection

from ..database import get_session
from . import router
from .models import PseudoTweet, Topics, Tweet
from .types import Month
from .word_cloud_helper import get_word_count_distribution


# Cache for 12 hours
@router.get("/")
@timed_lru_cache(seconds=12 * 60 * 60, maxsize=64)
def get_word_cloud(
    topics: Optional[Tuple[Topics, ...]] = Query(None),
    day: Optional[date] = None,
    month: Optional[Month] = None,
    session: Session = Depends(get_session),
):
    """
    Get the word-count distribution within the given time range
    """

    fields = ("text",)

    tweet_selection = get_filtered_selection(topics, Tweet, day, month, fields)
    pseudo_tweet_selection = get_filtered_selection(
        topics, PseudoTweet, day, month, fields
    )

    combined_model = union_all(tweet_selection, pseudo_tweet_selection).subquery().c

    # Manually selected the text here, need to change if needed
    combined_tweets = session.exec(select(combined_model.text)).all()

    # change list of tweets to tuple to allow caching
    word_freq = get_word_count_distribution(tuple(combined_tweets))

    return word_freq
