from datetime import date, datetime, timedelta
from typing import List, Optional

import nltk
import numpy as np
from fastapi import Depends, Query
from sqlmodel import Session, select, union_all

from ..database import get_session
from . import router
from .helper_functions import get_filtered_selection
from .models import PseudoTweet, Topics, Tweet
from .types import Month
from .word_cloud_helper import word_tokenize_nepali


@router.get("/")
def get_word_cloud(
    topics: Optional[List[Topics]] = Query(None),
    day: Optional[date] = None,
    month: Optional[Month] = None,
    session: Session = Depends(get_session),
):
    """
    Get the word-count distribution within the given time range
    """
    last_month = datetime.now() - timedelta(30)
    print(last_month)

    fields = ("text",)

    tweet_selection = get_filtered_selection(topics, Tweet, day, month, fields)
    pseudo_tweet_selection = get_filtered_selection(
        topics, PseudoTweet, day, month, fields
    )

    combined_model = union_all(tweet_selection, pseudo_tweet_selection).subquery().c

    # Manually selected the text here, need to change if needed
    combined_tweets = session.exec(select(combined_model.text)).all()

    tokens = tuple(map(word_tokenize_nepali, combined_tweets))

    tokens = np.hstack(np.array(tokens, dtype=object)).tolist()
    word_freq = nltk.FreqDist(tokens)

    return word_freq.most_common(100)
