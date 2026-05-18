from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.db import AudioFileModel, SnippetModel, SnippetTypeModel
from backend.service.audio_file import get_audio_file_path


@dataclass(frozen=True)
class RandomSnippetResult:
    snippet_id: int
    snippet_type_id: int
    snippet_type_name: str
    category: Optional[str]
    audio_file_id: int
    file_path: Path


def add_snippet_type(
    session: Session,
    *,
    name: str,
    category: Optional[str] = None,
) -> SnippetTypeModel:
    snippet_type = SnippetTypeModel(
        name=name,
        category=category,
    )

    session.add(snippet_type)
    session.commit()
    session.refresh(snippet_type)

    return snippet_type


def get_snippet_types(session: Session) -> list[SnippetTypeModel]:
    stmt = select(SnippetTypeModel).order_by(
        SnippetTypeModel.category.asc().nulls_last(),
        SnippetTypeModel.name.asc(),
    )

    return list(session.scalars(stmt).all())


def get_random_snippet_by_snippet_type(
    session: Session,
    *,
    storage_dir: Path,
    snippet_type_id: int,
) -> Optional[RandomSnippetResult]:
    stmt = (
        select(
            SnippetModel.id.label("snippet_id"),
            SnippetTypeModel.id.label("snippet_type_id"),
            SnippetTypeModel.name.label("snippet_type_name"),
            SnippetTypeModel.category.label("category"),
            AudioFileModel.id.label("audio_file_id"),
            AudioFileModel.file_extension.label("file_extension"),
        )
        .join(SnippetTypeModel, SnippetTypeModel.id == SnippetModel.snippet_type_id)
        .join(AudioFileModel, AudioFileModel.id == SnippetModel.audio_file_id)
        .where(SnippetModel.snippet_type_id == snippet_type_id)
        .order_by(func.random())
        .limit(1)
    )

    row = session.execute(stmt).one_or_none()
    if row is None:
        return None

    return RandomSnippetResult(
        snippet_id=row.snippet_id,
        snippet_type_id=row.snippet_type_id,
        snippet_type_name=row.snippet_type_name,
        category=row.category,
        audio_file_id=row.audio_file_id,
        file_path=get_audio_file_path(
            storage_dir=storage_dir,
            audio_file_id=row.audio_file_id,
            file_extension=row.file_extension or "",
        ),
    )


def delete_snippet_type(
    session: Session,
    *,
    snippet_type_id: int,
) -> bool:
    snippet_type = session.get(SnippetTypeModel, snippet_type_id)
    if snippet_type is None:
        return False

    if snippet_type.snippets:
        raise ValueError(
            f"Snippet type {snippet_type_id} is still used by snippets and cannot be deleted"
        )

    session.delete(snippet_type)
    session.commit()

    return True