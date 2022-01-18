from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Mount routers before database to read their database models
from .auth import router as auth_router
from .heroes import router as heroes_router
from .tweets import router as tweets_router

from .database import create_tables  # isort: skip

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Register API Routers here

app.include_router(auth_router)
app.include_router(heroes_router)
app.include_router(tweets_router)
