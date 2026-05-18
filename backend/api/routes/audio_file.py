from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.api.url import static_audio_url_for_path

from backend.api.deps import (
    get_audio_storage_dir,
    get_session,
)

from backend.service.audio_file import (
    add_audio_file,
    delete_audio_file,
    get_audio_file_by_id,
    get_audio_files,
)


router = APIRouter(
    prefix="/audio-files",
    tags=["Audio files"],
)


class AudioFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    artist: Optional[str] = None
    song: Optional[str] = None
    comment: Optional[str] = None
    mime_type: str
    file_extension: Optional[str] = None
    url: str


class AudioFilePageResponse(BaseModel):
    items: list[AudioFileResponse]
    total: int
    limit: int
    offset: int

class AudioFilePathResponse(BaseModel):
    id: int
    path: str
    url: str

def _response_from_audio_file(
    audio_file,
    *,
    storage_dir: Path,
) -> AudioFileResponse:
    path = storage_dir / f"{audio_file.id}{audio_file.file_extension or ''}"

    return AudioFileResponse(
        id=audio_file.id,
        artist=audio_file.artist,
        song=audio_file.song,
        comment=audio_file.comment,
        mime_type=audio_file.mime_type,
        file_extension=audio_file.file_extension,
        url=static_audio_url_for_path(path)
    )


@router.post(
    "",
    response_model=AudioFileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new audio file",
    description="Stores the uploaded file as `{id}{extension}` and creates the database record.",
)
def create_audio_file(
    file: UploadFile = File(..., description="Audio file to upload"),
    artist: Optional[str] = Form(None),
    song: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),
    session: Session = Depends(get_session),
    storage_dir: Path = Depends(get_audio_storage_dir),
) -> AudioFileResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename",
        )

    extension = Path(file.filename).suffix
    if not extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a file extension",
        )

    mime_type = file.content_type or "application/octet-stream"

    audio_file = add_audio_file(
        session,
        storage_dir=storage_dir,
        file_obj=file.file,
        artist=artist,
        song=song,
        comment=comment,
        mime_type=mime_type,
        file_extension=extension,
    )

    return _response_from_audio_file(
        audio_file,
        storage_dir=storage_dir,
    )


@router.get(
    "",
    response_model=AudioFilePageResponse,
    summary="Get all audio files",
    description="Returns audio files in a paginated list.",
)
def list_audio_files(
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
    storage_dir: Path = Depends(get_audio_storage_dir),
) -> AudioFilePageResponse:
    page = get_audio_files(
        session,
        limit=limit,
        offset=offset,
    )

    return AudioFilePageResponse(
        items=[
            _response_from_audio_file(
                audio_file,
                storage_dir=storage_dir,
            )
            for audio_file in page.items
        ],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )

@router.get(
    "/{audio_file_id}",
    response_model=AudioFileResponse,
    summary="Get audio file by ID",
    description="Returns one audio file by ID, including its public static URL.",
)
def get_audio_file(
    audio_file_id: int,
    session: Session = Depends(get_session),
    storage_dir: Path = Depends(get_audio_storage_dir),
) -> AudioFileResponse:
    audio_file = get_audio_file_by_id(
        session,
        audio_file_id=audio_file_id,
    )

    if audio_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audio file {audio_file_id} does not exist",
        )

    return _response_from_audio_file(
        audio_file,
        storage_dir=storage_dir,
    )

@router.delete(
    "/{audio_file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an audio file",
    description="Deletes the database record and removes the stored audio file.",
)
def remove_audio_file(
    audio_file_id: int,
    session: Session = Depends(get_session),
    storage_dir: Path = Depends(get_audio_storage_dir),
) -> None:
    deleted = delete_audio_file(
        session,
        storage_dir=storage_dir,
        audio_file_id=audio_file_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audio file {audio_file_id} does not exist",
        )