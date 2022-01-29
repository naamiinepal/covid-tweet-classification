from fastapi import APIRouter

router = APIRouter(prefix="/tweets", tags=["tweets"])

# Import all routes
from . import pseudo_routes  # noqa
from . import routes  # noqa
