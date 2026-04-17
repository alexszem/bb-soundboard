from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class TrackModel(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    artist: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    snippets: Mapped[list["SnippetModel"]] = relationship(
        back_populates="track",
        cascade="all, delete-orphan",
    )


class SnippetModel(Base):
    __tablename__ = "snippets"
    __table_args__ = (
        UniqueConstraint("track_id", "start_second", "stop_second", name="uq_snippet_song"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"), nullable=False)
    start_second: Mapped[int] = mapped_column(Integer, nullable=False)
    stop_second: Mapped[int] = mapped_column(Integer, nullable=False)

    track: Mapped["TrackModel"] = relationship(back_populates="snippets")
    usages: Mapped[list["UsageModel"]] = relationship(
        back_populates="snippet",
        cascade="all, delete-orphan",
    )


class UsageTypeModel(Base):
    __tablename__ = "usage_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    usages: Mapped[list["UsageModel"]] = relationship(back_populates="usage_type")


class UsageModel(Base):
    __tablename__ = "usages"
    __table_args__ = (
        UniqueConstraint("snippet_id", "usage_type_id", name="uq_usage_snippet_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snippet_id: Mapped[int] = mapped_column(ForeignKey("snippets.id"), nullable=False)
    usage_type_id: Mapped[int] = mapped_column(ForeignKey("usage_types.id"), nullable=False)

    snippet: Mapped["SnippetModel"] = relationship(back_populates="usages")
    usage_type: Mapped["UsageTypeModel"] = relationship(back_populates="usages")


class PlayerModel(Base):
    __tablename__ = "players"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    walkup_snippet_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("snippets.id"),
        nullable=True,
    )

    walkup_snippet: Mapped[Optional["SnippetModel"]] = relationship()