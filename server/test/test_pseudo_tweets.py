from datetime import datetime, timedelta
from typing import Tuple

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.tweets_common.models import PseudoTweet

from .tweets_common import list_tweets_helper, overview_helper

base_path = "/pseudo_tweets/"


@pytest.fixture(name="inserted_tweets")
def insert_tweets_fixture(session: Session):
    now = datetime.now()

    tweet1 = PseudoTweet(
        text="नारायणस्थानमा साउन ३१ सम्म निशेधाज्ञा",
        username="Hari Narayan Gautam",
        created_at=now,
        covid_stats=False,
        vaccination=False,
        covid_politics=False,
        humour=False,
        lockdown=1,
        civic_views=0,
        life_during_pandemic=False,
        covid_waves_and_variants=0,
    )
    tweet2 = PseudoTweet(
        text=(
            "गोरखामा बिहीबार पीसीआरबाट ७७ जना र"
            "एन्टिजेनबाट ३८ जनामा कोरोना संक्रमण पुष्टी"
        ),
        username="kailash babu sth",
        created_at=now - timedelta(days=1),
        covid_stats=1,
        vaccination=False,
        covid_politics=False,
        humour=False,
        lockdown=0,
        civic_views=0,
        life_during_pandemic=False,
        covid_waves_and_variants=0,
    )
    session.bulk_save_objects((tweet1, tweet2))
    session.commit()
    return tweet1, tweet2


def test_overview(inserted_tweets: Tuple[PseudoTweet, PseudoTweet], client: TestClient):
    overview_helper(base_path, inserted_tweets, client)


def test_list_tweets(
    inserted_tweets: Tuple[PseudoTweet, PseudoTweet], client: TestClient
):
    list_tweets_helper(base_path, inserted_tweets, client)
