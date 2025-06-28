from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.service.playback import PlaybackService
import os

router = APIRouter(prefix="/playback", tags=["Playback"])

playback_service = PlaybackService.get_instance()

@router.post("/stop")
def stop_song_route():
    playback_service.stop_song()
    return {"message": "Playback stopped successfully"}

@router.get("/song/{song_id}")
def get_song_file_route(song_id: int):
    # Adjust the songs directory path as needed for your project structure
    songs_dir = "../songs"
    # Retrieve file ending by scanning directory (assuming consistent naming)
    for file in os.listdir(songs_dir):
        if file.startswith(f"{song_id}."):
            file_path = os.path.join(songs_dir, file)
            return FileResponse(file_path, media_type="audio/mpeg", filename=file)
    raise HTTPException(status_code=404, detail="Song file not found")