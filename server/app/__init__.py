import os.path
from fastapi import FastAPI
from fastapi.responses import FileResponse
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


# Register API Routers here

app.include_router(auth_router)
app.include_router(heroes_router)
app.include_router(tweets_router)

# Directory to serve root files
files_dir = "templates"


@app.get("/{file_path:path}", response_class=FileResponse)
async def index(file_path: str):
    actual_path = os.path.join(files_dir, file_path)
    if os.path.isfile(actual_path):
        return actual_path
    return os.path.join(files_dir, "index.html")
