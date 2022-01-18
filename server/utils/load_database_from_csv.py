from datetime import datetime
from csv import DictReader

from app.database import get_session
from app.tweets.models import Tweet

with open("utils/nepali_tweets_dataset_vectors_EHnM_analysis_v1.csv") as csvfile:
    reader = DictReader(csvfile)
    tweets = []
    for row in reader:
        username = row["user_name"]
        created_at = datetime.strptime(row["created_at"], "%a %b %d %H:%M:%S %z %Y")
        kwargs = {**row, "username": username, "created_at": created_at}
        tweets.append(Tweet(**kwargs))

    session = next(get_session())
    session.add_all(tweets)
    session.commit()
