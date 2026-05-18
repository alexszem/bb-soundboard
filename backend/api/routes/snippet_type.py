from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.api.url import static_audio_url_for_path
from backend.api.deps import (
    get_audio_storage_dir,
    get_session,
)
from backend.service.snippet_type import (
    add_snippet_type,
    delete_snippet_type,
    get_random_snippet_by_snippet_type,
    get_snippet_types,
)

router = APIRouter(
    prefix="/snippet-types",
    tags=["Snippet types"],
)


class SnippetTypeCreateRequest(BaseModel):
    name: str
    category: Optional[str] = None


class SnippetTypeResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None


class RandomSnippetResponse(BaseModel):
    snippet_id: int
    snippet_type_id: int
    snippet_type_name: str
    category: Optional[str] = None
    audio_file_id: int
    url: str

@router.post(
    "",
    response_model=SnippetTypeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a snippet type",
    description="Creates a new snippet type such as `walkup`, `fail`, `goal`, or `celebration`.",
)
def create_snippet_type(
    request: SnippetTypeCreateRequest,
    session: Session = Depends(get_session),
) -> SnippetTypeResponse:
    snippet_type = add_snippet_type(
        session,
        name=request.name,
        category=request.category,
    )

    return SnippetTypeResponse(
        id=snippet_type.id,
        name=snippet_type.name,
        category=snippet_type.category,
    )


@router.get(
    "",
    response_model=list[SnippetTypeResponse],
    summary="Get all snippet types",
    description="Returns all available snippet types.",
)
def list_snippet_types(
    session: Session = Depends(get_session),
) -> list[SnippetTypeResponse]:
    snippet_types = get_snippet_types(session)

    return [
        SnippetTypeResponse(
            id=snippet_type.id,
            name=snippet_type.name,
            category=snippet_type.category,
        )
        for snippet_type in snippet_types
    ]


@router.get(
    "/{snippet_type_id}/random-snippet",
    response_model=RandomSnippetResponse,
    summary="Get a random snippet by snippet type",
    description="Returns one random snippet for the selected snippet type, including its static audio URL.",
)
def get_random_snippet(
    snippet_type_id: int,
    session: Session = Depends(get_session),
    storage_dir: Path = Depends(get_audio_storage_dir),
) -> RandomSnippetResponse:
    result = get_random_snippet_by_snippet_type(
        session,
        storage_dir=storage_dir,
        snippet_type_id=snippet_type_id,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No snippet found for snippet type {snippet_type_id}",
        )

    return RandomSnippetResponse(
        snippet_id=result.snippet_id,
        snippet_type_id=result.snippet_type_id,
        snippet_type_name=result.snippet_type_name,
        category=result.category,
        audio_file_id=result.audio_file_id,
        url=static_audio_url_for_path(result.file_path),
    )


@router.delete(
    "/{snippet_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a snippet type",
    description="Deletes a snippet type if it is not used by existing snippets.",
)
def remove_snippet_type(
    snippet_type_id: int,
    session: Session = Depends(get_session),
) -> None:
    try:
        deleted = delete_snippet_type(
            session,
            snippet_type_id=snippet_type_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Snippet type {snippet_type_id} does not exist",
        )