from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.db import PlayerModel, SnippetModel, TrackModel, UsageModel, UsageTypeModel


class TrackSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: Optional[str]
    artist: Optional[str]
    duration_seconds: Optional[int]

    @staticmethod
    def from_model(model: TrackModel) -> "TrackSchema":
        return TrackSchema(
            id=model.id,
            title=model.title,
            artist=model.artist,
            duration_seconds=model.duration_seconds,
        )


class SnippetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    track_id: int
    start_second: int
    stop_second: int

    @staticmethod
    def from_model(model: SnippetModel) -> "SnippetSchema":
        return SnippetSchema(
            id=model.id,
            track_id=model.track_id,
            start_second=model.start_second,
            stop_second=model.stop_second,
        )


class UsageTypeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: Optional[str]

    @staticmethod
    def from_model(model: UsageTypeModel) -> "UsageTypeSchema":
        return UsageTypeSchema(
            id=model.id,
            name=model.name,
            category=model.category,
        )


class UsageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    snippet_id: int
    usage_type_id: int

    @staticmethod
    def from_model(model: UsageModel) -> "UsageSchema":
        return UsageSchema(
            id=model.id,
            snippet_id=model.snippet_id,
            usage_type_id=model.usage_type_id,
        )


class PlayerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    walkup_snippet_id: Optional[int]

    @staticmethod
    def from_model(model: PlayerModel) -> "PlayerSchema":
        return PlayerSchema(
            name=model.name,
            walkup_snippet_id=model.walkup_snippet_id,
        )