from datetime import date
from typing import Optional, Tuple

import requests
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select, union_all

from app.config import settings
from app.tweets_common.decorators import timed_lru_cache
from app.tweets_common.helper_functions import get_filtered_selection

from ..database import get_session
from . import router
from .models import PredictionOutput, PseudoTweet, Topics, Tweet
from .types import Month
from .word_cloud_helper import get_word_count_distribution

CACHE_TIMEOUT = 6 * 60 * 60  # 6 hours


@router.get("/")
@timed_lru_cache(seconds=CACHE_TIMEOUT, maxsize=64)
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


THRESHOLD = (0.1002, 0.6141, 0.4196, 0.3442, 0.5132, 0.2217, 0.4631, 0.2109)


@router.get(
    "/predict",
    response_model=PredictionOutput,
    responses={503: {"description": "Could not connect to model."}},
)
@timed_lru_cache(seconds=CACHE_TIMEOUT, maxsize=64)
def get_prediction(text: str):
    """
    Get prediction from the live model
    """
    try:
        json_response = requests.post(
            settings.model_url, json={"instances": [text]}
        ).json()
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the model.")

    # We will be working on a single sample
    predictions = json_response["predictions"][0]

    labels = [pred >= thresh for pred, thresh in zip(predictions, THRESHOLD)]

    return PredictionOutput(predictions=predictions, labels=labels)
