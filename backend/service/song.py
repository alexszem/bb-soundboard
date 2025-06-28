import os
from werkzeug.utils import secure_filename
from backend.crud.song import add_song, get_song as get_song_crud, get_all_songs as get_all_songs_crud, delete_song as delete_song_crud
from mutagen import File as MutagenFile
from backend.utils import get_songs_dir  # for audio length extraction

# Song service layer
def is_valid_audio_file(file):
    valid_extensions = ['mp3', 'wav', 'ogg']  # extend as needed
    filename = secure_filename(file.filename)
    file_ending = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return file_ending in valid_extensions, file_ending

def get_audio_length(file_path: str) -> int:
    audio = MutagenFile(file_path)
    return int(audio.info.length) if audio and audio.info and hasattr(audio.info, 'length') else 0

def add_new_song(file, name: str, artist: str):
    is_valid, file_ending = is_valid_audio_file(file)
    if not is_valid:
        raise ValueError("Invalid audio file format.")

    songs_dir = get_songs_dir()

    temp_path = os.path.join(songs_dir, f"temp_upload.{file_ending}")
    file.save(temp_path)

    length = get_audio_length(temp_path)

    song_id = add_song(name=name, artist=artist, file_ending=file_ending, length=length)

    final_path = os.path.join(songs_dir, f"{song_id}.{file_ending}")
    os.rename(temp_path, final_path)

    return song_id

def delete_song(song_id: int):
    song = get_song_crud(song_id)
    if song:
        songs_dir = get_songs_dir()

        file_path = os.path.join(songs_dir, f"{song['id']}.{song['file_ending']}")
        if os.path.exists(file_path):
            os.remove(file_path)
        delete_song_crud(song_id)

def get_song(song_id: int):
    return get_song_crud(song_id)

def get_all_songs():
    return get_all_songs_crud()
