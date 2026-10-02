from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import init_db
from .routes import router


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

settings = get_settings()


# --------------------------------------------------
# APPLICATION STARTUP
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# --------------------------------------------------
# PROJECT DIRECTORY
# --------------------------------------------------

# main.py is inside:
# FITBUDDY-AI/app/main.py
#
# Therefore this points to:
# FITBUDDY-AI/app/

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    description="FitBuddy AI Fitness Plan Generator",
    version="1.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static",
)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

app.include_router(router)