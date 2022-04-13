from typing import Any, Callable, Optional, Tuple, TypeVar

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlmodel import Integer, Session, and_, func, not_, select, text, union_all

from .models import PseudoTweet, Topics, Tweet, TweetRead, TweetUpdate

import nltk
import re
import numpy as np

from . import STOP_WORDS


# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType", Tweet, PseudoTweet)


def get_filtered_selection(filter_topic: Optional[Topics], Model: ModelType):
    """
    Get selection query with filter depending upon filter_topic
    """
    selection = get_scalar_select(Model)

    if filter_topic is not None:
        filter = (
            text(
                Topics.others
            )  # Since others is defined in the selection, directly provide the column
            if filter_topic == Topics.others
            else getattr(Model, filter_topic)
        )
        selection = selection.filter(filter)
    return selection


def get_a_tweet(session: Session, tweet_id: PositiveInt, Model: ModelType) -> dict:
    """
    Get a not-None tweet from the database with others column as a dictonary
    """
    tweet = session.exec(
        get_scalar_select(Model).where(Model.id == tweet_id)
    ).one_or_none()

    assert_not_null(tweet, tweet_id, Model)

    return tweet


def make_tweet_read(tweet: ModelType, others: bool):
    """
    Make a TweetRead object from a Tweet or PseudoTweet row
    """
    return TweetRead.parse_obj(tweet.dict(), {"others": others})


def get_combined_tweet(
    session: Session, tweet_id: PositiveInt, Model: ModelType
) -> Tuple[ModelType, bool]:
    """
    Get a not-None combined tweet from the database with others column
    and model separated as tuple
    """
    tweet = session.exec(
        select(Model, get_others_column(Model)).where(Model.id == tweet_id)
    ).one_or_none()

    assert_not_null(tweet, tweet_id, Model)

    return tweet


def assert_not_null(tweet: Optional[ModelType], id: PositiveInt, Model: ModelType):
    """
    Make sure the provided row of tweet is not None
    """
    if tweet is None:
        raise HTTPException(404, f"{Model.__name__} with id: {id} not found.")


def get_scalar_select(Model: ModelType):
    """
    Get a select statement for the Model with others column
    """

    def get_model_attr(field: str):
        """
        Convert a field to Model.field
        """
        return getattr(Model, field)

    others_column = get_others_column(Model)
    scalar_tweet_attr = tuple(map(get_model_attr, Model.__fields__))
    return select(*scalar_tweet_attr, others_column)


def map_tweet_update(mapper_func: Callable[[str], Any]):
    """
    Return a tuple after mapping TweetUpdate fields (numeric fields)
    to mapper_func
    """
    return tuple(map(mapper_func, TweetUpdate.__fields__))


def get_others_column(Model: ModelType):
    """
    Get others column for the selection statement
    """

    def negate_columns(field: str):
        """
        Negate each field in the Model
        """
        return not_(getattr(Model, field))

    return and_(*map_tweet_update(negate_columns)).label("others")


def get_db_overview(session: Session, Model: ModelType):
    """
    Get overview of the database for the given Model
    """

    def get_overview_column(column: str):
        """
        Get a column for the selection of the overview
        """
        return func.sum(getattr(Model, column), type_=Integer).label(column)

    created_date = func.date(Model.created_at).label("created_date")
    others_column = get_others_column(Model)

    return session.exec(
        select(
            *map_tweet_update(get_overview_column),
            func.sum(others_column, type_=Integer).label("others"),
            created_date,
        ).group_by(created_date)
    ).all()


def get_all_overview(session: Session):
    """
    Get overview of the database for Tweet and PseudoTweet combined
    """

    def get_overview_selection(Model: ModelType):
        """
        Get the selection statement with numeric columns only and created_at
        """

        def get_model_attr(attr: str):
            return getattr(Model, attr)

        return select(
            *map_tweet_update(get_model_attr),
            Model.created_at,
        )

    all_model = (
        union_all(get_overview_selection(Tweet), get_overview_selection(PseudoTweet))
        .subquery()
        .c
    )

    return get_db_overview(session, all_model)

def remove_emojis(data: str):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def word_tokenize_nepali(text: str):
    text = remove_emojis(text)
    text = re.sub(r"\d+", ' ', text) # remove any digits
    text = re.sub(r"[,)({}[\]\.:;`_–\-``!‘’''“”?\-।/—%\|]+", ' ', text)
    text = re.sub(r"\s+", ' ', text) # replace multiple whitespaces with single whitespace
    text = text.replace("#", "").replace("_", " ") # remove #, and break words containing underscore
    text_tokens = [token for token in nltk.tokenize.word_tokenize(text) if token not in STOP_WORDS]
    return np.array(text_tokens)