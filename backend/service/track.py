from __future__ import annotations

import mimetypes
import os
import shutil
from pathlib import Path
from typing import BinaryIO, Optional, Protocol

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.db import (
    TrackModel,
)
from backend.service import Page, _paginate

TRACK_DATA_DIR = os.environ.get("TRACK_DATA_DIR", "./tracks")


class SupportsRead(Protocol):
    def read(self, size: int = -1) -> bytes: ...


class SupportsSeek(Protocol):
    def seek(self, offset: int, whence: int = 0) -> int: ...


FileLike = BinaryIO | SupportsRead

def _ensure_track_data_dir() -> Path:
    path = Path(TRACK_DATA_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _track_filename(track_id: int, mime_type: str) -> str:
    extension = mimetypes.guess_extension(mime_type) or ""
    return f"{track_id}{extension}"


def _track_path(track_id: int, mime_type: str) -> Path:
    return _ensure_track_data_dir() / _track_filename(track_id, mime_type)


def _rewind_if_possible(file: FileLike) -> None:
    if hasattr(file, "seek"):
        file.seek(0)


# ============================================================
# Track file helpers
# ============================================================

def extract_mimetype(file: FileLike, filename: Optional[str] = None) -> str:
    guessed_from_name: Optional[str] = None
    if filename:
        guessed_from_name, _ = mimetypes.guess_type(filename)

    if guessed_from_name:
        _rewind_if_possible(file)
        return guessed_from_name

    _rewind_if_possible(file)
    return "application/octet-stream"


def extract_duration(file: FileLike, filename: Optional[str] = None) -> int:
    """
    Placeholder implementation.

    Replace this later with real duration extraction, for example via:
    - mutagen
    - ffprobe
    - pydub / ffmpeg

    For now this returns 0 so the rest of the application can be built.
    """
    _rewind_if_possible(file)
    return 0


def save_track_to_disk(file: FileLike, filename: str) -> str:
    target_dir = _ensure_track_data_dir()
    target_path = target_dir / filename

    _rewind_if_possible(file)
    with open(target_path, "wb") as out_file:
        shutil.copyfileobj(file, out_file)

    _rewind_if_possible(file)
    return str(target_path)


# ============================================================
# Track business logic
# ============================================================

def get_tracks(
    session: Session,
    *,
    query: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Page[TrackModel]:
    stmt = select(TrackModel).order_by(TrackModel.id.asc())

    if query:
        pattern = f"%{query}%"
        stmt = stmt.where(
            or_(
                TrackModel.title.ilike(pattern),
                TrackModel.artist.ilike(pattern),
            )
        )

    return _paginate(session, stmt, TrackModel, limit=limit, offset=offset)

def add_track(
    session: Session,
    *,
    file: FileLike,
    title: Optional[str],
    artist: Optional[str],
    original_filename: Optional[str] = None,
) -> TrackModel:
    mime_type = extract_mimetype(file, original_filename)
    duration_seconds = extract_duration(file, original_filename)

    track = TrackModel(
        title=title,
        artist=artist,
        mime_type=mime_type,
        duration_seconds=duration_seconds,
    )
    session.add(track)
    session.flush()

    filename = _track_filename(track.id, track.mime_type)
    save_track_to_disk(file, filename)

    session.commit()
    session.refresh(track)
    return track


def delete_track(session: Session, track_id: int) -> bool:
    track = session.get(TrackModel, track_id)
    if track is None:
        return False

    file_path = _track_path(track.id, track.mime_type)

    session.delete(track)
    session.commit()

    if file_path.exists():
        file_path.unlink()

    return True