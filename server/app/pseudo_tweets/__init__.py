from fastapi import APIRouter

router = APIRouter(prefix="/pseudo_tweets", tags=["pseudo_tweets"])

# Import all routes
from . import routes  # noqa
