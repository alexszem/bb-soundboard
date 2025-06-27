from backend.crud.utils import with_session
from .snippet import get_snippet
from backend.models import Usage

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
def add_usage(session, snippet_id: int, usage_name: str):
    usage = Usage(snippet_id=snippet_id, usage_name=usage_name)
    session.add(usage)
    session.commit()
    return usage.id

@with_session
def edit_usage(session, usage_id: int, usage_name: str):
    usage = session.query(Usage).filter(Usage.id == usage_id).first()
    if usage:
        usage.usage_name = usage_name
        session.commit()

@with_session
def delete_usage(session, usage_id: int):
    usage = session.query(Usage).filter(Usage.id == usage_id).first()
    if usage:
        session.delete(usage)
        session.commit()

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