from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.audio import PlaybackController
from backend.db import (
    PlayerModel,
    SnippetModel,
)
from backend.service.snippet import play_snippet

def get_players(session: Session) -> list[PlayerModel]:
    stmt = select(PlayerModel).order_by(PlayerModel.name.asc())
    return list(session.scalars(stmt).all())

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


def update_player(
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


def delete_player(session: Session, name: str) -> bool:
    player = session.get(PlayerModel, name)
    if player is None:
        return False

    session.delete(player)
    session.commit()
    return True


def play_player_walkup(
    controller: PlaybackController,
    session: Session,
    player_name: str,
) -> bool:
    player = session.get(PlayerModel, player_name)
    if player is None or player.walkup_snippet_id is None:
        return False

    return play_snippet(controller, session, player.walkup_snippet_id)