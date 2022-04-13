from datetime import date
from typing import Any, Callable, List, Optional, Tuple, TypeVar

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlmodel import Integer, Session, and_, func, not_, select, text, union_all
from sqlmodel.sql.expression import Select

from .models import PseudoTweet, Topics, Tweet, TweetRead, TweetUpdate

# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType", Tweet, PseudoTweet)


def get_filtered_selection(
    topics: Optional[List[Topics]],
    day: Optional[date],
    Model: ModelType,
):
    """
    Get selection query with filter depending upon filter_topic
    """

    # Fail early
    if topics is not None and Topics.others in topics and len(topics) > 1:
        raise HTTPException(400, "Can't filter by others and other topics.")

    selection = get_scalar_select(Model)

    if topics is not None:
        for topic in topics:
            filter = (
                text(
                    Topics.others
                )  # Since others is defined in the selection, directly provide the column
                if topic == Topics.others
                else getattr(Model, topic)
            )
            selection = selection.filter(filter)

    if day is not None:
        selection = selection.filter(func.date(Model.created_at) == day)

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


def get_scalar_select(Model: ModelType) -> Select[tuple]:
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
