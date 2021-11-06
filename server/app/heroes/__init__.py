from fastapi import APIRouter

# Create a router for the heroes API
router = APIRouter(prefix="/heroes", tags=["heroes"])

# Import all routes
from . import routes  # noqa
