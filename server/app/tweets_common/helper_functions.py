from datetime import date
from typing import Callable, List, Optional, Tuple, TypeVar

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlmodel import Integer, Session, and_, func, not_, select, text, union_all
from sqlmodel.sql.expression import Select

from .models import PseudoTweet, Topics, Tweet, TweetRead, TweetUpdate
from .types import Month

import nltk
import re
import numpy as np

from . import STOP_WORDS


# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType", Tweet, PseudoTweet)


def get_filtered_selection(
    topics: Optional[List[Topics]],
    day: Optional[date],
    month: Optional[Month],
    Model: ModelType,
    fields: Optional[List[str]] = None,
):
    """
    Get selection query with filter depending upon topics provided
    """

    selection = get_scalar_select(Model, fields)

    if topics is not None:
        if Topics.others in topics:
            if len(topics) > 1:
                raise HTTPException(400, "Can't filter by others and other topics.")

            # If others is defined in the selection, directly provide the column
            filter = (
                text(Topics.others)
                if fields is None or not len(fields) or "others" in fields
                else get_others_column(Model)
            )
        else:
            filter = and_(*tuple(getattr(Model, topic) for topic in topics))

        selection = selection.filter(filter)

    if day is not None or month is not None:
        # If both specified, use day only
        filter = (
            func.date(Model.created_at) == day
            if day is not None
            else func.strftime("%Y-%m", Model.created_at) == month
        )
        selection = selection.filter(filter)

    return selection


def get_a_tweet(session: Session, tweet_id: PositiveInt, Model: ModelType) -> tuple:
    """
    Get a not-None tweet from the database with others column as a dictonary
    """
    tweet = session.exec(
        get_scalar_select(Model).where(Model.id == tweet_id)
    ).one_or_none()

    assert_not_null(tweet, tweet_id, Model)

    return tweet


def make_tweet_read(tweet: ModelType, others: bool) -> TweetRead:
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


def get_scalar_select(
    Model: ModelType, fields: Optional[List[str]] = None
) -> Select[tuple]:
    """
    Get a select statement for the Model with others column
    """

    is_fields_empty = fields is None or not len(fields)

    if is_fields_empty:
        fields = Model.__fields__

    db_fields = list(getattr(Model, field) for field in fields)

    if is_fields_empty or "others" in fields:
        db_fields.append(get_others_column(Model))

    return select(*db_fields)


MapperReturnType = TypeVar("MapperReturnType")


def map_tweet_update(
    mapper_func: Callable[[str], MapperReturnType]
) -> Tuple[MapperReturnType, ...]:
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


def get_db_overview(session: Session, Model: ModelType) -> List[tuple]:
    """
    Get overview of the database for the given Model
    """

    def get_overview_column(column: str):
        """
        Get a column for the selection of the overview
        """
        return func.sum(getattr(Model, column), type_=Integer).label(column)

    created_date_label = "created_date"
    created_date = func.date(Model.created_at).label(created_date_label)

    others_column = get_others_column(Model)

    return session.exec(
        select(
            *map_tweet_update(get_overview_column),
            func.sum(others_column, type_=Integer).label("others"),
            created_date,
        ).group_by(
            text(created_date_label)
        )  # Created_date is already defined
    ).all()


def get_all_overview(session: Session):
    """
    Get overview of the database for Tweet and PseudoTweet combined
    """

    def get_overview_selection(Model: ModelType) -> Select[tuple]:
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


async def remove_emojis(data: str):
    emoj = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        re.UNICODE,
    )
    return re.sub(emoj, "", data)


async def word_tokenize_nepali(text: str):
    text = await remove_emojis(text)
    text = re.sub(r"\d+", " ", text)  # remove any digits
    text = re.sub(r"[,)({}[\]\.:;`_–\-``!‘’''“”?\-।/—%\|]+", " ", text)
    text = re.sub(
        r"\s+", " ", text
    )  # replace multiple whitespaces with single whitespace
    text = text.replace("#", "").replace(
        "_", " "
    )  # remove #, and break words containing underscore
    text_tokens = [
        token for token in nltk.tokenize.word_tokenize(text) if token not in STOP_WORDS
    ]
    return np.array(text_tokens)
