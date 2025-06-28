from fastapi import APIRouter, UploadFile, Form, HTTPException

from backend.service.song import add_new_song, delete_song, get_all_songs, get_song

router = APIRouter(prefix="/songs", tags=["Songs"])

@router.post("/add")
def add_song_route(file: UploadFile, name: str = Form(...), artist: str = Form(...)):
    try:
        song_id = add_new_song(file, name, artist)
        return {"message": "Song added successfully", "song_id": song_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{song_id}")
def delete_song_route(song_id: int):
    delete_song(song_id)
    return {"message": "Song deleted successfully"}

@router.get("/{song_id}")
def get_song_route(song_id: int):
    song = get_song(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.get("/")
def get_all_songs_route():
    return get_all_songs()