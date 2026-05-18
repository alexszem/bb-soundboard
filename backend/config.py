from __future__ import annotations

import os
from pathlib import Path


DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./soundboard.db")

AUDIO_STORAGE_DIR = Path(
    os.environ.get("AUDIO_STORAGE_DIR", "./data/audio")
)

STATIC_AUDIO_URL_PREFIX = os.environ.get(
    "STATIC_AUDIO_URL_PREFIX",
    "/static/audio",
)