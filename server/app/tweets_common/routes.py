import typing
import pandas as pd
import numpy as np
import nltk


from typing import Optional

from fastapi import Depends
from sqlmodel import Session
from datetime import date, timedelta, datetime

from .models import Tweet, Topics, PseudoTweet
from . import router
from ..database import get_session
from .helper_functions import get_filtered_column_selection, word_tokenize_nepali


@router.get("/")
async def get_word_cloud(
    filter_topic: Optional[Topics] = None,
    filter_date: Optional[date] = None, # still need to work on this
    session: Session = Depends(get_session)
):
    """
    Get the word-count distribution within the given time range
    """
    last_month = datetime.now() - timedelta(30)
    print(last_month)
    selection_tweet = get_filtered_column_selection(filter_topic, PseudoTweet, ['text'])
    tweets = session.exec(
        selection_tweet
    ).all()
    selection_pseudo_tweet = get_filtered_column_selection(filter_topic, PseudoTweet, ['text'])
    pseudo_tweets = session.exec(
        selection_pseudo_tweet
    ).all()

    tokens = [await word_tokenize_nepali(elem) for elem in tweets+pseudo_tweets]
    tokens = np.hstack(np.array(tokens, dtype=object)).tolist()
    word_freq = nltk.FreqDist(tokens)

    return word_freq.most_common(100)
