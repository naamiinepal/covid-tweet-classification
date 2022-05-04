from datetime import date
from typing import Callable, Collection, List, Optional, Tuple, TypeVar

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlmodel import Integer, Session, and_, func, not_, select, text, union_all
from sqlmodel.sql.expression import Select

from .models import PseudoTweet, Topics, Tweet, TweetRead, TweetUpdate

# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType", Tweet, PseudoTweet)


def get_selection_filter(
    Model: ModelType,
    topics: Optional[Collection[Topics]],
    start_date: Optional[date],
    end_date: Optional[date],
    selection: Select[tuple],
    others_filter,
):
    """
    Filter the selection by various dimensions.
    `selection` is the selection before filtering
    `others_filter` signifies the filter to be used for others column.
    (direct text or creation of others column)
    """

    if topics is not None:
        if Topics.others in topics:
            if len(topics) > 1:
                raise HTTPException(400, "Can't filter by others and other topics.")

            # If others is defined in the selection, directly provide the column
            filter = others_filter
        else:
            filter = and_(*tuple(getattr(Model, topic) for topic in topics))

        selection = selection.filter(filter)

    created_date = func.date(Model.created_at)

    if start_date is not None:
        selection = selection.filter(created_date >= start_date)

    if end_date is not None:
        selection = selection.filter(created_date < end_date)
    return selection


def get_filtered_selection(
    Model: ModelType,
    topics: Optional[Collection[Topics]],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    fields: Optional[Collection[str]] = None,
):
    """
    Get selection query with filter depending upon topics provided
    """

    selection, contains_others = get_scalar_select(Model, fields)

    others_filter = text(Topics.others) if contains_others else get_others_column(Model)

    selection = get_selection_filter(
        Model, topics, start_date, end_date, selection, others_filter
    )

    return selection


def get_a_tweet(session: Session, tweet_id: PositiveInt, Model: ModelType) -> tuple:
    """
    Get a not-None tweet from the database with others column as a dictonary
    """

    selection, _ = get_scalar_select(Model).where(Model.id == tweet_id)

    tweet = session.exec(selection).one_or_none()

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
    Model: ModelType, fields: Optional[Collection[str]] = None
) -> Tuple[Select[tuple], bool]:
    """
    Get a select statement for the Model with others column
    """

    is_fields_empty = fields is None or not len(fields)

    if is_fields_empty:
        fields = Model.__fields__

    db_fields = list(getattr(Model, field) for field in fields)

    contains_others = is_fields_empty or "others" in fields

    if contains_others:
        db_fields.append(get_others_column(Model))

    return select(*db_fields), contains_others


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
            func.count().label("total"),
        ).group_by(
            text(created_date_label)
        )  # Created_date is already defined
    ).all()


def get_combined_model():

    """
    Get a combined model with numerics columns and created_at
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
    return all_model


def get_filtered_count(
    Model: ModelType,
    topics: Optional[Collection[Topics]],
    start_date: Optional[date],
    end_date: Optional[date],
    session: Session,
):
    def get_sum_column(column: str):
        """
        Get a column for the selection of the overview
        """
        # May return None if there are no matching rows to filters.
        # So, colascing NULL to 0.
        return func.coalesce(func.sum(getattr(Model, column), type_=Integer), 0).label(
            column
        )

    others_column = get_others_column(Model)

    selection = select(
        *map_tweet_update(get_sum_column),
        func.coalesce(func.sum(others_column, type_=Integer), 0).label("others"),
        func.count().label("total"),
    )

    others_filter = text(Topics.others)

    selection = get_selection_filter(
        Model, topics, start_date, end_date, selection, others_filter
    )

    return session.exec(selection).one()
