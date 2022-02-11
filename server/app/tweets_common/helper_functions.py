from typing import Any, Callable, Optional, Tuple, TypeVar

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlmodel import Integer, Session, and_, func, not_, select, union

from .models import PseudoTweet, Tweet, TweetRead, TweetUpdate

# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType", Tweet, PseudoTweet)


def get_a_tweet(session: Session, tweet_id: PositiveInt, Model: ModelType) -> dict:
    tweet = session.exec(
        get_scalar_select(Model).where(Model.id == tweet_id)
    ).one_or_none()

    assert_not_null(tweet, tweet_id)

    return tweet


def make_tweet_read(tweet: ModelType, others: bool):
    return TweetRead.from_orm(tweet, {"others": others})


def get_combined_tweet(
    session: Session, tweet_id: PositiveInt, Model: ModelType
) -> Tuple[ModelType, bool]:
    tweet = session.exec(
        select(Model, get_others_column(Model)).where(Model.id == tweet_id)
    ).one_or_none()

    assert_not_null(tweet, tweet_id)

    return tweet


def assert_not_null(tweet: Optional[ModelType], id: PositiveInt):
    if tweet is None:
        raise HTTPException(404, f"{tweet.__name__} with id: {id} not found.")


def get_scalar_select(Model: ModelType):
    def get_model_attr(field: str):
        return getattr(Model, field)

    others_column = get_others_column(Model)
    scalar_tweet_attr = tuple(map(get_model_attr, Model.__fields__))
    return select(*scalar_tweet_attr, others_column)


def map_tweet_update(mapper_func: Callable[[str], Any]):
    return tuple(map(mapper_func, TweetUpdate.__fields__))


def get_others_column(Model: ModelType):
    def negate_columns(field: str):
        return not_(getattr(Model, field))

    return and_(*map_tweet_update(negate_columns)).label("others")


def get_db_overview(session: Session, Model: ModelType):
    def get_overview_row(column: str):
        return func.sum(getattr(Model, column), type_=Integer).label(column)

    created_date = func.date(Model.created_at).label("created_date")
    others_column = get_others_column(Model)

    return session.exec(
        select(
            *map_tweet_update(get_overview_row),
            func.sum(others_column, type_=Integer).label("others"),
            created_date,
        ).group_by(created_date)
    ).all()


def get_all_overview(session: Session):
    def get_overview_selection(Model: ModelType):
        def get_model_attr(attr: str):
            return getattr(Model, attr)

        return select(
            *map_tweet_update(get_model_attr),
            Model.created_at,
        )

    all_model = (
        union(get_overview_selection(Tweet), get_overview_selection(PseudoTweet))
        .subquery()
        .c
    )

    return get_db_overview(session, all_model)
