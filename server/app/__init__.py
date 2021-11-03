from fastapi import FastAPI

from . import models  # noqa
from .database import create_tables
from .hero_routes import router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router)
