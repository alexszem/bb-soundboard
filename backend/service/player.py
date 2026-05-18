from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import AudioFileModel, PlayerModel, SnippetModel
from backend.service.audio_file import get_audio_file_path


@dataclass(frozen=True)
class PlayerListItem:
    name: str
    walkup_snippet_id: Optional[int]
    walkup_snippet_path: Optional[Path]


def add_player(
    session: Session,
    *,
    name: str,
    walkup_snippet_id: Optional[int] = None,
) -> PlayerModel:
    if walkup_snippet_id is not None and session.get(SnippetModel, walkup_snippet_id) is None:
        raise ValueError(f"Snippet {walkup_snippet_id} does not exist")

    player = PlayerModel(
        name=name,
        walkup_snippet_id=walkup_snippet_id,
    )

    session.add(player)
    session.commit()
    session.refresh(player)

    return player


def get_players(
    session: Session,
    *,
    storage_dir: Path,
) -> list[PlayerListItem]:
    stmt = (
        select(
            PlayerModel.name.label("name"),
            PlayerModel.walkup_snippet_id.label("walkup_snippet_id"),
            AudioFileModel.id.label("audio_file_id"),
            AudioFileModel.file_extension.label("file_extension"),
        )
        .outerjoin(SnippetModel, SnippetModel.id == PlayerModel.walkup_snippet_id)
        .outerjoin(AudioFileModel, AudioFileModel.id == SnippetModel.audio_file_id)
        .order_by(PlayerModel.name.asc())
    )

    rows = session.execute(stmt).all()

    return [
        PlayerListItem(
            name=row.name,
            walkup_snippet_id=row.walkup_snippet_id,
            walkup_snippet_path=(
                get_audio_file_path(
                    storage_dir=storage_dir,
                    audio_file_id=row.audio_file_id,
                    file_extension=row.file_extension or "",
                )
                if row.audio_file_id is not None
                else None
            ),
        )
        for row in rows
    ]


def update_player_walkup_snippet(
    session: Session,
    *,
    name: str,
    walkup_snippet_id: Optional[int],
) -> Optional[PlayerModel]:
    player = session.get(PlayerModel, name)
    if player is None:
        return None

    if walkup_snippet_id is not None and session.get(SnippetModel, walkup_snippet_id) is None:
        raise ValueError(f"Snippet {walkup_snippet_id} does not exist")

    player.walkup_snippet_id = walkup_snippet_id

    session.commit()
    session.refresh(player)

    return player


def delete_player(
    session: Session,
    *,
    name: str,
) -> bool:
    player = session.get(PlayerModel, name)
    if player is None:
        return False

    session.delete(player)
    session.commit()

    return True