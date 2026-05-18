from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import AudioFileModel, PlayerModel, SnippetModel, SnippetTypeModel
from backend.service.audio_file import get_audio_file_path
from backend.service.pagination import Page, paginate_rows


@dataclass(frozen=True)
class SnippetListItem:
    id: int
    audio_file_id: int
    snippet_type_id: int
    snippet_type_name: str
    category: Optional[str]
    file_path: Path


def add_snippet(
    session: Session,
    *,
    audio_file_id: int,
    snippet_type_id: int,
) -> SnippetModel:
    if session.get(AudioFileModel, audio_file_id) is None:
        raise ValueError(f"Audio file {audio_file_id} does not exist")

    if session.get(SnippetTypeModel, snippet_type_id) is None:
        raise ValueError(f"Snippet type {snippet_type_id} does not exist")

    snippet = SnippetModel(
        audio_file_id=audio_file_id,
        snippet_type_id=snippet_type_id,
    )

    session.add(snippet)
    session.commit()
    session.refresh(snippet)

    return snippet


def get_snippets(
    session: Session,
    *,
    storage_dir: Path,
    snippet_type_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
) -> Page[SnippetListItem]:
    stmt = (
        select(
            SnippetModel.id,
            SnippetModel.audio_file_id,
            SnippetModel.snippet_type_id,
            SnippetTypeModel.name,
            SnippetTypeModel.category,
            AudioFileModel.file_extension,
        )
        .join(AudioFileModel, AudioFileModel.id == SnippetModel.audio_file_id)
        .join(SnippetTypeModel, SnippetTypeModel.id == SnippetModel.snippet_type_id)
        .order_by(SnippetModel.id.desc())
    )

    if snippet_type_id is not None:
        stmt = stmt.where(SnippetModel.snippet_type_id == snippet_type_id)

    page = paginate_rows(
        session,
        stmt,
        limit=limit,
        offset=offset,
    )

    return Page(
        items=[
            SnippetListItem(
                id=row.id,
                audio_file_id=row.audio_file_id,
                snippet_type_id=row.snippet_type_id,
                snippet_type_name=row.name,
                category=row.category,
                file_path=get_audio_file_path(
                    storage_dir=storage_dir,
                    audio_file_id=row.audio_file_id,
                    file_extension=row.file_extension or "",
                ),
            )
            for row in page.items
        ],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )


def delete_snippet(
    session: Session,
    *,
    snippet_id: int,
) -> bool:
    snippet = session.get(SnippetModel, snippet_id)
    if snippet is None:
        return False

    players_stmt = select(PlayerModel).where(
        PlayerModel.walkup_snippet_id == snippet.id,
    )
    players = list(session.scalars(players_stmt).all())

    for player in players:
        player.walkup_snippet_id = None

    session.delete(snippet)
    session.commit()

    return True