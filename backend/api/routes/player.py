from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.api.url import static_audio_url_for_path
from backend.api.deps import (
    get_audio_storage_dir,
    get_session,
)
from backend.service.player import (
    add_player,
    delete_player,
    get_players,
    update_player_walkup_snippet,
)


router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


class PlayerCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    walkup_snippet_id: Optional[int] = None


class PlayerUpdateWalkupSnippetRequest(BaseModel):
    walkup_snippet_id: Optional[int] = None


class PlayerResponse(BaseModel):
    name: str
    walkup_snippet_id: Optional[int] = None


class PlayerListItemResponse(BaseModel):
    name: str
    walkup_snippet_id: Optional[int] = None
    walkup_snippet_url: Optional[str] = None


@router.post(
    "",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a player",
    description="Creates a player and optionally assigns a walkup snippet.",
)
def create_player(
    request: PlayerCreateRequest,
    session: Session = Depends(get_session),
) -> PlayerResponse:
    try:
        player = add_player(
            session,
            name=request.name,
            walkup_snippet_id=request.walkup_snippet_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return PlayerResponse(
        name=player.name,
        walkup_snippet_id=player.walkup_snippet_id,
    )


@router.get(
    "",
    response_model=list[PlayerListItemResponse],
    summary="Get all players",
    description="Returns all players, including the static URL of their walkup snippet if one is assigned.",
)
def list_players(
    session: Session = Depends(get_session),
    storage_dir: Path = Depends(get_audio_storage_dir),
) -> list[PlayerListItemResponse]:
    players = get_players(
        session,
        storage_dir=storage_dir,
    )

    return [
        PlayerListItemResponse(
            name=player.name,
            walkup_snippet_id=player.walkup_snippet_id,
            walkup_snippet_url=(
                static_audio_url_for_path(player.walkup_snippet_path)
                if player.walkup_snippet_path is not None
                else None
            ),
        )
        for player in players
    ]


@router.patch(
    "/{name}/walkup-snippet",
    response_model=PlayerResponse,
    summary="Update player walkup snippet",
    description="Updates or clears the walkup snippet for a player.",
)
def update_walkup_snippet(
    name: str,
    request: PlayerUpdateWalkupSnippetRequest,
    session: Session = Depends(get_session),
) -> PlayerResponse:
    try:
        player = update_player_walkup_snippet(
            session,
            name=name,
            walkup_snippet_id=request.walkup_snippet_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player {name} does not exist",
        )

    return PlayerResponse(
        name=player.name,
        walkup_snippet_id=player.walkup_snippet_id,
    )


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a player",
    description="Deletes a player.",
)
def remove_player(
    name: str,
    session: Session = Depends(get_session),
) -> None:
    deleted = delete_player(
        session,
        name=name,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player {name} does not exist",
        )