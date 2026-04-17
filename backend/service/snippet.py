from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.audio import PlaybackController
from backend.db import (
    SnippetModel,
    TrackModel,
)
from backend.service import Page, _paginate

def get_snippets(
    session: Session,
    *,
    track_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
) -> Page[SnippetModel]:
    stmt = select(SnippetModel).order_by(SnippetModel.id.asc())

    if track_id is not None:
        stmt = stmt.where(SnippetModel.track_id == track_id)

    return _paginate(session, stmt, SnippetModel, limit=limit, offset=offset)

def add_snippet(
    session: Session,
    *,
    track_id: int,
    start_second: int,
    stop_second: int,
) -> SnippetModel:
    if start_second < 0:
        raise ValueError("start_second must be >= 0")
    if stop_second <= start_second:
        raise ValueError("stop_second must be > start_second")

    track = session.get(TrackModel, track_id)
    if track is None:
        raise ValueError(f"Track {track_id} does not exist")

    if stop_second > track.duration_seconds:
        raise ValueError("stop_second exceeds track duration")

    snippet = SnippetModel(
        track_id=track_id,
        start_second=start_second,
        stop_second=stop_second,
    )
    session.add(snippet)
    session.commit()
    session.refresh(snippet)
    return snippet


def add_snippets(
    session: Session,
    *,
    snippets: Sequence[tuple[int, int, int]],
) -> list[SnippetModel]:
    created: list[SnippetModel] = []

    for track_id, start_second, stop_second in snippets:
        if start_second < 0:
            raise ValueError("start_second must be >= 0")
        if stop_second <= start_second:
            raise ValueError("stop_second must be > start_second")

        track = session.get(TrackModel, track_id)
        if track is None:
            raise ValueError(f"Track {track_id} does not exist")
        if stop_second > track.duration_seconds:
            raise ValueError("stop_second exceeds track duration")

        created.append(
            SnippetModel(
                track_id=track_id,
                start_second=start_second,
                stop_second=stop_second,
            )
        )

    session.add_all(created)
    session.commit()

    for snippet in created:
        session.refresh(snippet)

    return created


def delete_snippet(session: Session, snippet_id: int) -> bool:
    snippet = session.get(SnippetModel, snippet_id)
    if snippet is None:
        return False

    session.delete(snippet)
    session.commit()
    return True


def queue_snippet(controller: PlaybackController, session: Session, snippet_id: int) -> bool:
    snippet = session.get(SnippetModel, snippet_id)
    if snippet is None:
        return False

    controller.queue_track(
        snippet.track_id,
        snippet.start_second,
        snippet.stop_second,
        overlap=None,
    )
    return True


def play_snippet(controller: PlaybackController, session: Session, snippet_id: int) -> bool:
    queued = queue_snippet(controller, session, snippet_id)
    if not queued:
        return False

    controller.play()
    return True