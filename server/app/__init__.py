import os.path
from functools import lru_cache

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Mount routers before database to read their database models
from .auth import router as auth_router
from .pseudo_tweets import router as pseudo_router
from .tweets import router as tweets_router

from .database import create_tables  # isort: skip

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    create_tables()


# Register API Routers here
app.include_router(auth_router)
app.include_router(pseudo_router)
app.include_router(tweets_router)


# Cache the output for maximum 10 items
@lru_cache(maxsize=10)
def get_actual_path(filename: str):
    return os.path.join("templates", filename)


@app.get("/{file_path:path}", response_class=FileResponse)
async def index(file_path: str):
    actual_path = get_actual_path(file_path)
    if os.path.isfile(actual_path):
        return actual_path
    return get_actual_path("index.html")
