from fastapi import APIRouter

router = APIRouter(prefix="/tweets", tags=["tweets"])

# Import all routes
from . import routes  # noqa
