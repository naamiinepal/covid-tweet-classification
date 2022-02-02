from csv import DictReader
from datetime import datetime
from random import randrange
from typing import List, Mapping, Union

from sqlmodel import Session, select

from app.auth.models import User
from app.database import get_session
from app.tweets.models import Tweet

with open("utils/nepali_tweets_dataset_vectors_EHnM_v2_with_annotator.csv") as csvfile:
    tweets: List[Tweet] = []
    session: Session = next(get_session())
    email_to_id: Mapping[str, int] = {}
    for row in DictReader(csvfile):
        created_at: datetime = datetime.strptime(
            row["created_at"], "%a %b %d %H:%M:%S %z %Y"
        )

        verifier_email = row["annotator"]

        # Try to get from cache
        verifier_id = email_to_id.get(verifier_email)

        # If cache misses
        if verifier_id is None:
            # Get from database
            verifier_id = session.exec(
                select(User.id).where(User.email == verifier_email)
            ).one()
            # And update the cache
            email_to_id[verifier_email] = verifier_id

        # Get a random datetime each time from within the range
        verified_at = datetime(
            year=2021,
            month=randrange(10, 12),
            day=randrange(1, 31),
            hour=randrange(8, 22),
            minute=randrange(0, 60),
            second=randrange(0, 60),
            microsecond=randrange(0, 1_000_000),
        )

        kwargs: Mapping[str, Union[str, int, datetime]] = {
            **row,
            "created_at": created_at,
            "verifier_id": verifier_id,
            "verified_at": verified_at,
        }
        tweets.append(Tweet(**kwargs))

session.bulk_save_objects(tweets)
session.commit()
