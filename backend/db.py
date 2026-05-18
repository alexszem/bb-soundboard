from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AudioFileModel(Base):
    __tablename__ = "audio_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    artist: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    song: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    file_extension: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    snippets: Mapped[list["SnippetModel"]] = relationship(
        back_populates="audio_file",
        cascade="all, delete-orphan",
    )


class SnippetTypeModel(Base):
    __tablename__ = "snippet_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    snippets: Mapped[list["SnippetModel"]] = relationship(
        back_populates="snippet_type",
        cascade="all, delete-orphan",
    )


class SnippetModel(Base):
    __tablename__ = "snippets"
    __table_args__ = (
        UniqueConstraint(
            "audio_file_id",
            "snippet_type_id",
            name="uq_snippet_file_type",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    audio_file_id: Mapped[int] = mapped_column(
        ForeignKey("audio_files.id"),
        nullable=False,
    )
    snippet_type_id: Mapped[int] = mapped_column(
        ForeignKey("snippet_types.id"),
        nullable=False,
    )

    audio_file: Mapped["AudioFileModel"] = relationship(
        back_populates="snippets",
    )
    snippet_type: Mapped["SnippetTypeModel"] = relationship(
        back_populates="snippets",
    )

    players_using_as_walkup: Mapped[list["PlayerModel"]] = relationship(
        back_populates="walkup_snippet",
    )


class PlayerModel(Base):
    __tablename__ = "players"

    name: Mapped[str] = mapped_column(String, primary_key=True)

    walkup_snippet_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("snippets.id"),
        nullable=True,
    )

    walkup_snippet: Mapped[Optional["SnippetModel"]] = relationship(
        back_populates="players_using_as_walkup",
    )