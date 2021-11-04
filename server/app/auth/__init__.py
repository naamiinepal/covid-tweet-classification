from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

from . import routes  # noqa
