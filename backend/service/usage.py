from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.audio import PlaybackController, play_snippet
from backend.db import (
    SnippetModel,
    UsageModel,
    UsageTypeModel,
)
from backend.service import Page, _paginate

def get_usages(
    session: Session,
    *,
    usage_type_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
) -> Page[UsageModel]:
    stmt = select(UsageModel).order_by(UsageModel.id.asc())

    if usage_type_id is not None:
        stmt = stmt.where(UsageModel.usage_type_id == usage_type_id)

    return _paginate(session, stmt, UsageModel, limit=limit, offset=offset)

def add_usage(
    session: Session,
    *,
    snippet_id: int,
    usage_type_id: int,
) -> UsageModel:
    snippet = session.get(SnippetModel, snippet_id)
    if snippet is None:
        raise ValueError(f"Snippet {snippet_id} does not exist")

    usage_type = session.get(UsageTypeModel, usage_type_id)
    if usage_type is None:
        raise ValueError(f"Usage type {usage_type_id} does not exist")

    usage = UsageModel(
        snippet_id=snippet_id,
        usage_type_id=usage_type_id,
    )
    session.add(usage)
    session.commit()
    session.refresh(usage)
    return usage


def delete_usage(session: Session, usage_id: int) -> bool:
    usage = session.get(UsageModel, usage_id)
    if usage is None:
        return False

    session.delete(usage)
    session.commit()
    return True


def play_usage(controller: PlaybackController, session: Session, usage_id: int) -> bool:
    usage = session.get(UsageModel, usage_id)
    if usage is None:
        return False

    return play_snippet(controller, session, usage.snippet_id)