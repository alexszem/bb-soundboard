from backend.crud.utils import with_session
from backend.models import Song

@with_session
def get_song(session, song_id: int):
    song = session.query(Song).filter(Song.id == song_id).first()
    if song:
        return {
            "id": song.id,
            "name": song.name,
            "artist": song.artist,
            "file_ending": song.file_ending,
            "length": song.length
        }
    return None

@with_session
def add_song(session, name: str, artist: str, file_ending: str, length: int):
    song = Song(name=name, artist=artist, file_ending=file_ending, length=length)
    session.add(song)
    session.commit()
    return song.id

@with_session
def delete_song(session, song_id: int):
    song = session.query(Song).filter(Song.id == song_id).first()
    if song:
        session.delete(song)
        session.commit()

@with_session
def get_all_songs(session):
    songs = session.query(Song).all()
    result = []
    for song in songs:
        result.append({
            "id": song.id,
            "name": song.name,
            "artist": song.artist,
            "file_ending": song.file_ending,
            "length": song.length
        })
    return result