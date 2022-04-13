import typing
import pandas as pd
import numpy as np
import nltk


from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from .models import Tweet, Topics, PseudoTweet
from . import router
from ..database import get_session
from .helper_functions import get_filtered_selection, word_tokenize_nepali


@router.get("/")
async def get_word_cloud(
    filter_topic: Optional[Topics] = None,
    session: Session = Depends(get_session),
):
    """
    Get the word-count distribution within the given time range
    """
    selection = get_filtered_selection(filter_topic, PseudoTweet)

    tweets = session.exec(
        selection
    ).all()
    tweets_df = pd.DataFrame(tweets)
    # tweets_df.drop_duplicates(subset=['text'], keep='last', inplace=True, ignore_index=True)
    tokens = tweets_df['text'].map(word_tokenize_nepali)
    tokens = np.hstack(np.array(tokens)).tolist()
    word_freq = nltk.FreqDist(tokens)

    return word_freq.most_common(100)
