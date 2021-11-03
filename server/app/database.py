from typing import Optional, TypeVar

from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine

database_url = "sqlite:///db.sqlite3"

# The main point is, by ensuring you don't share the same session with more than one
# request, the code is already safe.
engine = create_engine(
    database_url, connect_args={"check_same_thread": False}, echo=True
)

# Make a Generic Type to get the original type completion back
ModelType = TypeVar("ModelType")


def get_or_404(session: Session, model: ModelType, id: int) -> ModelType:
    row: Optional[SQLModel] = session.get(model, id)
    if row is None:
        raise HTTPException(404, f"{model.__name__} with id: {id} not found.")
    return row


def save_and_refresh(session: Session, model: SQLModel):
    session.add(model)
    session.commit()
    session.refresh(model)


def create_tables():
    SQLModel.metadata.create_all(engine)


# Database related dependency
def get_session():
    with Session(engine) as session:
        yield session
