from sqlmodel import Integer, Session, func, select, union

from app.tweets.models import PseudoTweet, Tweet, TweetBase, TweetUpdate


def get_db_overview(session: Session, model: TweetBase):
    def get_overview_row(column: str):
        return func.sum(getattr(model, column), type_=Integer).label(column)

    created_date = func.date(model.created_at).label("created_date")

    return session.exec(
        select(
            *tuple(map(get_overview_row, TweetUpdate.__fields__)),
            created_date,
        ).group_by(created_date)
    ).all()


def get_all_overview(session: Session):
    def get_overview_selection(model: TweetBase):
        def get_model_attr(attr: str):
            return getattr(model, attr)

        return select(
            *tuple(map(get_model_attr, TweetUpdate.__fields__)),
            model.created_at,
        )

    all_model = (
        union(get_overview_selection(Tweet), get_overview_selection(PseudoTweet))
        .subquery()
        .c
    )

    return get_db_overview(session, all_model)
