from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import AudioFileModel, PlayerModel, SnippetModel
from backend.service.pagination import Page, paginate_scalars


def _normalize_extension(file_extension: str) -> str:
    extension = file_extension.strip().lower()

    if not extension:
        raise ValueError("file_extension must not be empty")

    if not extension.startswith("."):
        extension = f".{extension}"

    return extension


def get_audio_file_path(
    *,
    storage_dir: Path,
    audio_file_id: int,
    file_extension: str,
) -> Path:
    return storage_dir / f"{audio_file_id}{file_extension}"


def get_audio_file_path_for_id(
    session: Session,
    *,
    storage_dir: Path,
    audio_file_id: int,
) -> Optional[Path]:
    audio_file = session.get(AudioFileModel, audio_file_id)
    if audio_file is None:
        return None

    return get_audio_file_path(
        storage_dir=storage_dir,
        audio_file_id=audio_file.id,
        file_extension=audio_file.file_extension or "",
    )

def get_audio_file_by_id(
    session: Session,
    *,
    audio_file_id: int,
) -> Optional[AudioFileModel]:
    return session.get(AudioFileModel, audio_file_id)

def add_audio_file(
    session: Session,
    *,
    storage_dir: Path,
    file_obj: BinaryIO,
    artist: Optional[str] = None,
    song: Optional[str] = None,
    comment: Optional[str] = None,
    mime_type: str,
    file_extension: str,
) -> AudioFileModel:
    extension = _normalize_extension(file_extension)

    storage_dir.mkdir(parents=True, exist_ok=True)

    audio_file = AudioFileModel(
        artist=artist,
        song=song,
        comment=comment,
        mime_type=mime_type,
        file_extension=extension,
    )

    try:
        session.add(audio_file)
        session.flush()

        target_path = get_audio_file_path(
            storage_dir=storage_dir,
            audio_file_id=audio_file.id,
            file_extension=extension,
        )

        with target_path.open("wb") as target_file:
            shutil.copyfileobj(file_obj, target_file)

        session.commit()
        session.refresh(audio_file)
        return audio_file

    except Exception:
        session.rollback()

        if audio_file.id is not None:
            target_path = get_audio_file_path(
                storage_dir=storage_dir,
                audio_file_id=audio_file.id,
                file_extension=extension,
            )
            target_path.unlink(missing_ok=True)

        raise


def get_audio_files(
    session: Session,
    *,
    limit: int = 50,
    offset: int = 0,
) -> Page[AudioFileModel]:
    stmt = select(AudioFileModel).order_by(AudioFileModel.id.desc())

    return paginate_scalars(
        session,
        stmt,
        limit=limit,
        offset=offset,
    )


def delete_audio_file(
    session: Session,
    *,
    storage_dir: Path,
    audio_file_id: int,
) -> bool:
    audio_file = session.get(AudioFileModel, audio_file_id)
    if audio_file is None:
        return False

    file_path = get_audio_file_path(
        storage_dir=storage_dir,
        audio_file_id=audio_file.id,
        file_extension=audio_file.file_extension or "",
    )

    snippet_ids_stmt = select(SnippetModel.id).where(
        SnippetModel.audio_file_id == audio_file.id,
    )
    snippet_ids = list(session.scalars(snippet_ids_stmt).all())

    if snippet_ids:
        players_stmt = select(PlayerModel).where(
            PlayerModel.walkup_snippet_id.in_(snippet_ids),
        )
        players = list(session.scalars(players_stmt).all())

        for player in players:
            player.walkup_snippet_id = None

    session.delete(audio_file)
    session.commit()

    file_path.unlink(missing_ok=True)

    return True