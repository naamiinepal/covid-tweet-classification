from typing import List

from app.tweets_common.models import PseudoTweet, Tweet

from utils.load_labels import load_database as load_label
from utils.load_pseudo_labels import load_database as load_pseudo_label

from sqlmodel import Session
from sqlalchemy.exc import OperationalError


def test_labels(session: Session):
    # Test suite may not contain the database to get the verifier id
    try:
        tweets: List[Tweet] = load_label(session)
    except OperationalError as e:
        assert "no such table: user" in str(e)
    else:
        assert isinstance(tweets, list)
        assert len(tweets) > 0
        assert all(isinstance(t, Tweet) for t in tweets)


def test_pseudo_labels(session: Session):
    pseudo_tweets: List[PseudoTweet] = load_pseudo_label(session)

    assert isinstance(pseudo_tweets, list)
    assert len(pseudo_tweets) > 0
    assert all(isinstance(pt, PseudoTweet) for pt in pseudo_tweets)
