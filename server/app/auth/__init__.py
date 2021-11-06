from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# Import all routes
from . import routes  # noqa
