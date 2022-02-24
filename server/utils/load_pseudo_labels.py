from csv import DictReader
from datetime import datetime
from typing import List, Mapping, Union

from sqlmodel import Session

from app.database import get_session
from app.tweets_common.models import PseudoTweet

with open("utils/pseudo_label_dataset_feb_23.csv") as csvfile:
    pseudo_tweets: List[PseudoTweet] = []
    for row in DictReader(csvfile):
        created_at: datetime = datetime.strptime(
            row["created_at"], r"%a %b %d %H:%M:%S %z %Y"
        )
        kwargs: Mapping[str, Union[str, datetime]] = {
            **row,
            "created_at": created_at,
        }
        pseudo_tweets.append(PseudoTweet(**kwargs))

session: Session = next(get_session())
session.bulk_save_objects(pseudo_tweets)
session.commit()
