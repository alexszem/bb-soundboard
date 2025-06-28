import os

def get_songs_dir() -> str:
    songs_dir = os.path.join(os.path.dirname(__file__), 'songs')
    return os.path.abspath(songs_dir)