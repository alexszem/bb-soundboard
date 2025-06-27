import os
from backend.crud.snippet import add_snippet as add_snippet_crud, delete_snippet as delete_snippet_crud, edit_snippet as edit_snippet_crud, get_snippet as get_snippet_crud, get_all_snippets as get_all_snippets_crud
from backend.crud.song import get_song
from .playback import PlaybackService  # adjust import path as needed

# Snippet service layer with validation and playback
def add_new_snippet(song_id: int, start: int = None, stop: int = None):
    song = get_song(song_id)
    if not song:
        raise ValueError("Song does not exist.")

    # Default start to 0 if None, stop to song length if None
    start = start if start is not None else 0
    stop = stop if stop is not None else song['length']

    validate_snippet_times(start, stop, song['length'])

    snippet_id = add_snippet_crud(song_id=song_id, start=start, stop=stop)
    return snippet_id

def edit_existing_snippet(snippet_id: int, start: int = None, stop: int = None):
    snippet = get_snippet_crud(snippet_id)
    if not snippet:
        raise ValueError("Snippet does not exist.")

    song = snippet['song']
    # Default start to 0 if None, stop to song length if None
    start = start if start is not None else 0
    stop = stop if stop is not None else song['length']

    validate_snippet_times(start, stop, song['length'])

    edit_snippet_crud(snippet_id, start, stop)

def delete_snippet(snippet_id: int):
    delete_snippet_crud(snippet_id)

def play_snippet(snippet_id: int):
    snippet = get_snippet_crud(snippet_id)
    if not snippet:
        raise ValueError("Snippet does not exist.")

    song = snippet['song']
    file_path = os.path.join("../songs", f"{song['id']}.{song['file_ending']}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    playback_service = PlaybackService.get_instance()
    duration = snippet['stop'] - snippet['start']
    playback_service.play_song(file_path, start=snippet['start'], duration=duration)

def get_snippet(snippet_id: int):
    return get_snippet_crud(snippet_id)

def get_all_snippets():
    return get_all_snippets_crud()

# Utility function for snippet validation
def validate_snippet_times(start: int, stop: int, song_length: int):
    if start < 0 or stop < 0:
        raise ValueError("Start and stop times must be non-negative.")
    if start >= stop:
        raise ValueError("Start time must be less than stop time.")
    if stop > song_length:
        raise ValueError("Stop time exceeds song length.")