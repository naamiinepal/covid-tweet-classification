from typing import List

from fastapi import Depends, Query
from sqlmodel import Session, select

from app.database import get_or_404, get_session, save_and_refresh

from . import router
from .models import Hero, HeroCreate, HeroRead, HeroUpdate


@router.post("/", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    """
    Create a new hero.
    """
    db_hero = Hero.from_orm(hero)
    save_and_refresh(session, db_hero)
    return db_hero


@router.get("/", response_model=List[HeroRead])
def read_heroes(
    offset: int = 0,
    limit: int = Query(default=10, lt=11),
    session: Session = Depends(get_session),
):
    """
    Read heroes within the offset and limit
    """
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get(
    "/{hero_id}",
    response_model=HeroRead,
    responses={404: {"description": "Hero Not found"}},
)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    """
    Read a hero by id.
    """
    hero = get_or_404(session, Hero, hero_id)
    return hero


@router.patch(
    "/{hero_id}",
    response_model=HeroRead,
    responses={404: {"description": "Hero Not found"}},
)
def update_hero(
    hero_id: int, hero: HeroUpdate, session: Session = Depends(get_session)
):
    """
    Update a hero by id.
    """
    db_hero = get_or_404(session, Hero, hero_id)

    # Exclude the ones not sent by the client
    hero_data = hero.dict(exclude_unset=True)

    for key, value in hero_data.items():
        setattr(db_hero, key, value)

    save_and_refresh(session, db_hero)
    return db_hero


@router.delete("/{hero_id}", responses={404: {"description": "Hero Not found"}})
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    """
    Delete a hero by id.
    """
    hero = get_or_404(session, Hero, hero_id)

    session.delete(hero)
    session.commit()
    return {"ok": True}
