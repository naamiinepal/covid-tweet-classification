from fastapi import APIRouter

router = APIRouter(prefix="/tweets_commons", tags=["tweets_commons"])

# get all the stopwords
with open("stopwords.txt") as fp:
    STOP_WORDS = set(fp.read().splitlines())

# Import all routes
from . import routes  # noqa
