from csv import DictReader
from datetime import datetime, timezone
from typing import List, Mapping, Union

from sqlmodel import Session

from app.database import get_session
from app.tweets.models import Tweet

with open("utils/nepali_tweets_dataset_vectors_EHnM_analysis_v2.csv") as csvfile:
    now: datetime = datetime.now(timezone.utc)
    tweets: List[Tweet] = []
    for row in DictReader(csvfile):
        created_at: datetime = datetime.strptime(
            row["created_at"], "%a %b %d %H:%M:%S %z %Y"
        )
        kwargs: Mapping[str, Union[str, int, datetime]] = {
            **row,
            "created_at": created_at,
            "verifier_id": 1,
            "verified_at": now,
        }
        tweets.append(Tweet(**kwargs))

session: Session = next(get_session())
session.bulk_save_objects(tweets)
session.commit()
