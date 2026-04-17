from __future__ import annotations

import random
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.audio import PlaybackController
from backend.db import (
    UsageModel,
    UsageTypeModel,
)
from backend.service.snippet import queue_snippet

def get_usage_types(session: Session) -> list[UsageTypeModel]:
    stmt = select(UsageTypeModel).order_by(UsageTypeModel.name.asc())
    return list(session.scalars(stmt).all())

def add_usage_type(
    session: Session,
    *,
    name: str,
    category: Optional[str] = None,
) -> UsageTypeModel:
    usage_type = UsageTypeModel(name=name, category=category)
    session.add(usage_type)
    session.commit()
    session.refresh(usage_type)
    return usage_type


def delete_usage_type(session: Session, usage_type_id: int) -> bool:
    usage_type = session.get(UsageTypeModel, usage_type_id)
    if usage_type is None:
        return False

    session.delete(usage_type)
    session.commit()
    return True


def play_usage_type(
    controller: PlaybackController,
    session: Session,
    usage_type_id: int,
) -> bool:
    stmt = select(UsageModel).where(UsageModel.usage_type_id == usage_type_id)
    usages = list(session.scalars(stmt).all())

    if not usages:
        return False

    chosen = random.choice(usages)

    controller.stop()
    queued = queue_snippet(controller, session, chosen.snippet_id)
    if not queued:
        return False
    controller.play()
    return True