from backend.crud.utils import with_session
from .song import get_song
from backend.models import Snippet

@with_session
def get_snippet(session, snippet_id: int):
    snippet = session.query(Snippet).filter(Snippet.id == snippet_id).first()
    if snippet:
        song_data = get_song(snippet.song_id)
        return {
            "id": snippet.id,
            "start": snippet.start,
            "stop": snippet.stop,
            "song": song_data
        }
    return None

@with_session
def get_snippets_by_song(session, song_id: int):
    snippets = session.query(Snippet).filter(Snippet.song_id == song_id).all()
    return [{
        "id": snippet.id,
        "start": snippet.start,
        "stop": snippet.stop
    } for snippet in snippets]

@with_session
def get_all_snippets(session):
    snippets = session.query(Snippet).all()
    result = []
    for snippet in snippets:
        song_data = get_song(snippet.song_id)
        result.append({
            "id": snippet.id,
            "start": snippet.start,
            "stop": snippet.stop,
            "song": song_data
        })
    return result

@with_session
def add_snippet(session, song_id: int, start: int, stop: int):
    snippet = Snippet(song_id=song_id, start=start, stop=stop)
    session.add(snippet)
    session.commit()
    return snippet.id

@with_session
def edit_snippet(session, snippet_id: int, start: int, stop: int):
    snippet = session.query(Snippet).filter(Snippet.id == snippet_id).first()
    if snippet:
        snippet.start = start
        snippet.stop = stop
        session.commit()

@with_session
def delete_snippet(session, snippet_id: int):
    snippet = session.query(Snippet).filter(Snippet.id == snippet_id).first()
    if snippet:
        session.delete(snippet)
        session.commit()