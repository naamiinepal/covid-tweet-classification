from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from .database import get_or_404, get_session, save_and_refresh
from .models import Hero, HeroCreate, HeroRead, HeroUpdate

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post("/", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.from_orm(hero)
    save_and_refresh(session, db_hero)
    return db_hero


@router.get("/", response_model=List[HeroRead])
def read_heroes(
    offset: int = 0,
    limit: int = Query(default=10, lt=11),
    session: Session = Depends(get_session),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get(
    "/{hero_id}",
    response_model=HeroRead,
    responses={404: {"description": "Hero Not found"}},
)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
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
    db_hero = get_or_404(session, Hero, hero_id)

    # Exclude the ones not sent by the client
    hero_data = hero.dict(exclude_unset=True)

    for key, value in hero_data.items():
        setattr(db_hero, key, value)

    save_and_refresh(session, db_hero)
    return db_hero


@router.delete("/{hero_id}", responses={404: {"description": "Hero Not found"}})
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = get_or_404(session, Hero, hero_id)

    session.delete(hero)
    session.commit()
    return {"ok": True}
