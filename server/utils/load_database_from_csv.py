from csv import DictReader
from datetime import datetime

from app.database import get_session
from app.tweets.models import Tweet

with open("utils/nepali_tweets_dataset_vectors_EHnM_analysis_v2.csv") as csvfile:
    reader = DictReader(csvfile)
    tweets = []
    for row in reader:
        created_at = datetime.strptime(row["created_at"], "%a %b %d %H:%M:%S %z %Y")
        kwargs = {**row, "created_at": created_at}
        tweets.append(Tweet(**kwargs))

    session = next(get_session())
    session.add_all(tweets)
    session.commit()
