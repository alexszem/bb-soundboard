from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.api.deps import (
    create_database_tables,
    get_audio_storage_dir,
    seed_required_data,
)
from backend.api.routes.audio_file import router as audio_file_router
from backend.api.routes.player import router as player_router
from backend.api.routes.snippet import router as snippet_router
from backend.api.routes.snippet_type import router as snippet_type_router
from backend.config import STATIC_AUDIO_URL_PREFIX


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()
    seed_required_data()
    get_audio_storage_dir()
    yield


app = FastAPI(
    title="Soundboard API",
    description="Backend API for managing audio files, snippets, snippet types, and players.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    STATIC_AUDIO_URL_PREFIX,
    StaticFiles(directory=get_audio_storage_dir()),
    name="static-audio",
)


app.include_router(audio_file_router)
app.include_router(snippet_router)
app.include_router(snippet_type_router)
app.include_router(player_router)


@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
)
def health_check() -> dict[str, str]:
    return {"status": "ok"}

HTML_DIR = Path("./html")

app.mount(
    "/assets",
    StaticFiles(directory=HTML_DIR / "assets"),
    name="frontend-assets",
)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(HTML_DIR / "index.html")