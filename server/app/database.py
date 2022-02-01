from typing import Optional, TypeVar

from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine

from .config import settings

# The main point is, by ensuring you don't share the same session with more than one
# request, the code is already safe.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=settings.database_echo,
)

# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType")


def get_or_404(session: Session, model: ModelType, id: int) -> ModelType:
    """
    Get a model by id or raise a 404 error
    """
    row: Optional[SQLModel] = session.get(model, id)
    if row is None:
        raise HTTPException(404, f"{model.__name__} with id: {id} not found.")
    return row


def save_and_refresh(session: Session, model: SQLModel, refresh: bool = True):
    """
    Save a model and refresh it to get the latest data
    """
    session.add(model)
    session.commit()
    if refresh:
        session.refresh(model)


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
