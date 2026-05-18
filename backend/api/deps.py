from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from backend.config import AUDIO_STORAGE_DIR, DATABASE_URL
from backend.db import Base, SnippetTypeModel

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_database_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_audio_storage_dir() -> Path:
    AUDIO_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    return AUDIO_STORAGE_DIR

def seed_required_data() -> None:
    with SessionLocal() as session:
        required_snippet_types = [
            {
                "id": 1,
                "name": "Intermission",
                "category": "Hidden",
            },
            {
                "id": 2,
                "name": "Walkup",
                "category": "Hidden",
            },
        ]

        for snippet_type_data in required_snippet_types:
            snippet_type = session.get(
                SnippetTypeModel,
                snippet_type_data["id"],
            )

            if snippet_type is None:
                snippet_type = SnippetTypeModel(
                    id=snippet_type_data["id"],
                    name=snippet_type_data["name"],
                    category=snippet_type_data["category"],
                )
                session.add(snippet_type)
            else:
                snippet_type.name = snippet_type_data["name"]
                snippet_type.category = snippet_type_data["category"]

        session.commit()