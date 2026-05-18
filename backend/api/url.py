from pathlib import Path

from backend.config import STATIC_AUDIO_URL_PREFIX

def static_audio_url_for_path(path: Path) -> str:
    return f"{STATIC_AUDIO_URL_PREFIX.rstrip('/')}/{path.name}"