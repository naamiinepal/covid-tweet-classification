from fastapi import APIRouter
import os

router = APIRouter(prefix="/commons", tags=["commons"])
# get all the stopwords
with open("stopwords.txt", mode='r') as fp:
    STOP_WORDS = set(line.strip() for line in fp)

# Import all routes
from . import routes  # noqa
