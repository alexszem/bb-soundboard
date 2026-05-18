from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.api.url import static_audio_url_for_path
from backend.api.deps import (
    get_audio_storage_dir,
    get_session,
)
from backend.service.snippet import (
    add_snippet,
    delete_snippet,
    get_snippets,
)


router = APIRouter(
    prefix="/snippets",
    tags=["Snippets"],
)


class SnippetCreateRequest(BaseModel):
    audio_file_id: int
    snippet_type_id: int


class SnippetResponse(BaseModel):
    id: int
    audio_file_id: int
    snippet_type_id: int


class SnippetListItemResponse(BaseModel):
    id: int
    audio_file_id: int
    snippet_type_id: int
    snippet_type_name: str
    category: Optional[str] = None
    url: str


class SnippetPageResponse(BaseModel):
    items: list[SnippetListItemResponse]
    total: int
    limit: int
    offset: int


@router.post(
    "",
    response_model=SnippetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a snippet",
    description="Creates a snippet that connects an audio file with a snippet type.",
)
def create_snippet(
    request: SnippetCreateRequest,
    session: Session = Depends(get_session),
) -> SnippetResponse:
    try:
        snippet = add_snippet(
            session,
            audio_file_id=request.audio_file_id,
            snippet_type_id=request.snippet_type_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return SnippetResponse(
        id=snippet.id,
        audio_file_id=snippet.audio_file_id,
        snippet_type_id=snippet.snippet_type_id,
    )


@router.get(
    "",
    response_model=SnippetPageResponse,
    summary="Get all snippets",
    description="Returns snippets with optional snippet-type filtering, pagination, category, and static audio URL.",
)
def list_snippets(
    snippet_type_id: Optional[int] = Query(
        None,
        description="Optional snippet type filter",
    ),
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
    storage_dir: Path = Depends(get_audio_storage_dir),
) -> SnippetPageResponse:
    page = get_snippets(
        session,
        storage_dir=storage_dir,
        snippet_type_id=snippet_type_id,
        limit=limit,
        offset=offset,
    )

    return SnippetPageResponse(
        items=[
            SnippetListItemResponse(
                id=item.id,
                audio_file_id=item.audio_file_id,
                snippet_type_id=item.snippet_type_id,
                snippet_type_name=item.snippet_type_name,
                category=item.category,
                url=static_audio_url_for_path(item.file_path),
            )
            for item in page.items
        ],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )


@router.delete(
    "/{snippet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a snippet",
    description="Deletes a snippet. Players using this snippet as walkup sound are cleared.",
)
def remove_snippet(
    snippet_id: int,
    session: Session = Depends(get_session),
) -> None:
    deleted = delete_snippet(
        session,
        snippet_id=snippet_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Snippet {snippet_id} does not exist",
        )