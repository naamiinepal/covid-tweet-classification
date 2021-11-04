from fastapi import APIRouter

router = APIRouter(prefix="/heroes", tags=["heroes"])

from . import routes  # noqa
