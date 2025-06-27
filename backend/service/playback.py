import pygame
import threading
import time

class PlaybackService:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        pygame.mixer.init()
        self.currently_playing = None
        self.stop_timer = None

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def play_song(self, file_path: str, start: float = 0.0, duration: float = None):
        self.stop_song()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(start=start)
        self.currently_playing = file_path

        if duration is not None:
            def stop_after_duration():
                time.sleep(duration)
                self.stop_song()

            self.stop_timer = threading.Thread(target=stop_after_duration)
            self.stop_timer.start()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.currently_playing = None
        if self.stop_timer and self.stop_timer.is_alive():
            # No direct kill for thread, just let it finish or ignore
            self.stop_timer = None

    def is_playing(self):
        return pygame.mixer.music.get_busy()