from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session


T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int


def paginate_scalars(
    session: Session,
    stmt,
    *,
    limit: int = 50,
    offset: int = 0,
) -> Page[T]:
    safe_limit = max(1, min(limit, 500))
    safe_offset = max(0, offset)

    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = session.scalar(total_stmt) or 0

    items = list(session.scalars(stmt.limit(safe_limit).offset(safe_offset)).all())

    return Page(
        items=items,
        total=total,
        limit=safe_limit,
        offset=safe_offset,
    )


def paginate_rows(
    session: Session,
    stmt,
    *,
    limit: int = 50,
    offset: int = 0,
) -> Page:
    safe_limit = max(1, min(limit, 500))
    safe_offset = max(0, offset)

    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = session.scalar(total_stmt) or 0

    items = list(session.execute(stmt.limit(safe_limit).offset(safe_offset)).all())

    return Page(
        items=items,
        total=total,
        limit=safe_limit,
        offset=safe_offset,
    )