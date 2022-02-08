from typing import Optional, TypeVar

from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from .config import settings

# The main point is, by ensuring you don't share the same session with more than one
# request, the code is already safe.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=settings.database_echo,
)

# Fix Unncessary caching warning for now. Refer to
# https://github.com/tiangolo/sqlmodel/issues/189 for more info

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType")


def get_or_404(session: Session, Model: ModelType, id: int) -> ModelType:
    """
    Get a model by id or raise a 404 error
    """
    row: Optional[SQLModel] = session.get(Model, id)
    if row is None:
        raise HTTPException(404, f"{Model.__name__} with id: {id} not found.")
    return row


def save_and_refresh(session: Session, row: SQLModel, refresh: bool = True):
    """
    Save a model and refresh it to get the latest data
    """
    session.add(row)
    session.commit()
    if refresh:
        session.refresh(row)


def create_tables():
    """
    Create all tables in the database
    """
    SQLModel.metadata.create_all(engine)


# Database related dependency
def get_session():
    """
    Get a session from the engine
    """
    with Session(engine) as session:
        yield session
