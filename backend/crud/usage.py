from backend.crud.utils import with_session
from .snippet import get_snippet
from backend.models import Usage
from sqlalchemy.exc import IntegrityError

@with_session
def get_usage(session, usage_id: int):
    usage = session.query(Usage).filter(Usage.id == usage_id).first()
    if usage:
        snippet_data = get_snippet(usage.snippet_id)
        return {
            "id": usage.id,
            "usage": usage.usage_name,
            "snippet": snippet_data
        }
    return None

@with_session
def get_usages_by_name(session, usage_name: str):
    usages = session.query(Usage).filter(Usage.usage_name == usage_name).all()
    result = []
    for usage in usages:
        result.append({
            "id": usage.id,
            "usage": usage.usage_name,
            "snippet_id": usage.snippet_id
        })
    return result

@with_session
def get_usage_names_for_snippet(session, snippet_id: int):
    usages = session.query(Usage).filter(Usage.snippet_id == snippet_id).all()
    return [usage.usage_name for usage in usages]

@with_session
def add_usage(session, snippet_id: int, usage_name: str):
    usage = Usage(snippet_id=snippet_id, usage_name=usage_name)
    session.add(usage)
    try:
        session.commit()
        return usage.id
    except IntegrityError:
        session.rollback()
        # Optionally return existing usage id or a meaningful error
        existing = session.query(Usage).filter(
            Usage.snippet_id == snippet_id,
            Usage.usage_name == usage_name
        ).first()
        return existing.id if existing else None

@with_session
def delete_usage(session, usage_id: int):
    usage = session.query(Usage).filter(Usage.id == usage_id).first()
    if usage:
        session.delete(usage)
        session.commit()

@with_session
def set_usages_for_snippet(session, snippet_id: int, usage_names: list):
    # Fetch existing usages for this snippet
    existing_usages = session.query(Usage).filter(Usage.snippet_id == snippet_id).all()
    existing_names = set(u.usage_name for u in existing_usages)
    new_names = set(usage_names)

    # Delete usages not in new_names
    for usage in existing_usages:
        if usage.usage_name not in new_names:
            session.delete(usage)

    # Add new usages not in existing_names
    for name in new_names:
        if name not in existing_names:
            new_usage = Usage(snippet_id=snippet_id, usage_name=name)
            session.add(new_usage)

    session.commit()
    return {
        "snippet_id": snippet_id,
        "updated_usages": list(new_names)
    }

@with_session
def get_all_usages(session):
    usages = session.query(Usage).all()
    result = []
    for usage in usages:
        snippet_data = get_snippet(usage.snippet_id)
        result.append({
            "id": usage.id,
            "usage": usage.usage_name,
            "snippet": snippet_data
        })
    return result