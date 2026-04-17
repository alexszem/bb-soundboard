from __future__ import annotations

import mimetypes
import os
import threading
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, TypeVar

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import GLib, Gst  # noqa: E402


TRACK_DATA_DIR = os.environ.get("TRACK_DATA_DIR", "./tracks")


@dataclass(frozen=True)
class QueuedTrack:
    track_id: int
    start_second: int
    stop_second: int
    overlap: Optional[int] = None


@dataclass(frozen=True)
class PlaybackStatus:
    is_playing: bool
    current_track_id: Optional[int]
    position_second: Optional[float]
    queue_length: int
    volume: float


_T = TypeVar("_T")


class PlaybackController:
    def __init__(
        self,
        *,
        track_data_dir: str = TRACK_DATA_DIR,
        poll_interval_ms: int = 100,
    ) -> None:
        Gst.init(None)

        self._track_data_dir = Path(track_data_dir)
        self._track_data_dir.mkdir(parents=True, exist_ok=True)

        self._poll_interval_ms = poll_interval_ms
        self._lock = threading.RLock()

        self._queue: deque[QueuedTrack] = deque()
        self._current_item: Optional[QueuedTrack] = None
        self._is_playing: bool = False
        self._volume: float = 1.0

        self._loop = GLib.MainLoop()
        self._loop_thread = threading.Thread(
            target=self._loop.run,
            name="playback-controller-glib",
            daemon=True,
        )

        self._playbin = Gst.ElementFactory.make("playbin", "player")
        if self._playbin is None:
            raise RuntimeError("Failed to create GStreamer playbin")

        self._playbin.set_property("volume", self._volume)

        self._bus = self._playbin.get_bus()
        if self._bus is None:
            raise RuntimeError("Failed to get GStreamer bus")

        self._bus.add_signal_watch()
        self._bus.connect("message", self._on_bus_message)

        self._position_timer_id: Optional[int] = None
        self._seek_pending: bool = False
        self._shutdown: bool = False

        self._loop_thread.start()
        self._run_on_loop(self._ensure_position_timer)

    def queue_track(
        self,
        track_id: int,
        start_second: int,
        stop_second: int,
        overlap: Optional[int] = None,
    ) -> None:
        if start_second < 0:
            raise ValueError("start_second must be >= 0")
        if stop_second <= start_second:
            raise ValueError("stop_second must be > start_second")
        if overlap is not None and overlap < 0:
            raise ValueError("overlap must be >= 0")

        item = QueuedTrack(
            track_id=track_id,
            start_second=start_second,
            stop_second=stop_second,
            overlap=overlap,
        )

        def op() -> None:
            with self._lock:
                self._queue.append(item)

        self._run_on_loop(op)

    def clear_queue(self) -> None:
        def op() -> None:
            with self._lock:
                self._queue.clear()

        self._run_on_loop(op)

    def play(self) -> None:
        def op() -> None:
            with self._lock:
                if self._current_item is None:
                    self._advance_to_next_locked()
                    return

                result = self._playbin.set_state(Gst.State.PLAYING)
                self._raise_on_state_change_failure(result, "play")
                self._is_playing = True

        self._run_on_loop(op)

    def pause(self) -> None:
        def op() -> None:
            with self._lock:
                result = self._playbin.set_state(Gst.State.PAUSED)
                self._raise_on_state_change_failure(result, "pause")
                self._is_playing = False

        self._run_on_loop(op)

    def stop(self) -> None:
        def op() -> None:
            with self._lock:
                self._stop_locked(clear_queue=True)

        self._run_on_loop(op)

    def get_volume(self) -> float:
        def op() -> float:
            with self._lock:
                return self._volume

        return self._run_on_loop(op)

    def set_volume(self, volume: float) -> None:
        if not 0.0 <= volume <= 1.0:
            raise ValueError("volume must be between 0.0 and 1.0")

        def op() -> None:
            with self._lock:
                self._volume = volume
                self._playbin.set_property("volume", volume)

        self._run_on_loop(op)

    def get_current_status(self) -> PlaybackStatus:
        def op() -> PlaybackStatus:
            with self._lock:
                position_second: Optional[float] = None
                if self._current_item is not None:
                    position_second = self._query_position_seconds()

                return PlaybackStatus(
                    is_playing=self._is_playing,
                    current_track_id=None if self._current_item is None else self._current_item.track_id,
                    position_second=position_second,
                    queue_length=len(self._queue),
                    volume=self._volume,
                )

        return self._run_on_loop(op)

    def shutdown(self) -> None:
        def op() -> None:
            with self._lock:
                if self._shutdown:
                    return
                self._shutdown = True
                self._stop_locked(clear_queue=True)
                if self._position_timer_id is not None:
                    GLib.source_remove(self._position_timer_id)
                    self._position_timer_id = None
                self._bus.remove_signal_watch()
                self._loop.quit()

        self._run_on_loop(op, allow_after_shutdown=True)
        if self._loop_thread.is_alive():
            self._loop_thread.join(timeout=2.0)

    def __del__(self) -> None:
        try:
            if not self._shutdown:
                self.shutdown()
        except Exception:
            pass

    def _run_on_loop(
        self,
        func: Callable[[], _T],
        *,
        allow_after_shutdown: bool = False,
    ) -> _T:
        if self._shutdown and not allow_after_shutdown:
            raise RuntimeError("PlaybackController is shut down")

        done = threading.Event()
        result: dict[str, object] = {}

        def wrapper() -> bool:
            try:
                result["value"] = func()
            except BaseException as exc:
                result["error"] = exc
            finally:
                done.set()
            return False

        GLib.idle_add(wrapper)
        done.wait()

        if "error" in result:
            raise result["error"]  # type: ignore[misc]

        return result["value"]  # type: ignore[return-value]

    def _ensure_position_timer(self) -> None:
        if self._position_timer_id is None:
            self._position_timer_id = GLib.timeout_add(
                self._poll_interval_ms,
                self._poll_position,
            )

    def _poll_position(self) -> bool:
        with self._lock:
            if self._shutdown:
                return False

            if self._current_item is None:
                return True

            if not self._is_playing:
                return True

            position_seconds = self._query_position_seconds()
            if position_seconds is None:
                return True

            if position_seconds >= float(self._current_item.stop_second):
                self._advance_to_next_locked()

            return True

    def _on_bus_message(self, _bus: Gst.Bus, message: Gst.Message) -> None:
        def op() -> None:
            with self._lock:
                if self._shutdown:
                    return

                if message.type == Gst.MessageType.ERROR:
                    err, debug = message.parse_error()
                    self._stop_locked(clear_queue=False)
                    raise RuntimeError(f"GStreamer error: {err}. Debug: {debug}")

                if message.type == Gst.MessageType.EOS:
                    self._advance_to_next_locked()
                    return

                if message.type == Gst.MessageType.ASYNC_DONE:
                    if self._seek_pending and self._current_item is not None:
                        self._seek_pending = False
                        self._seek_to_current_start_locked()
                    return

                if message.type == Gst.MessageType.STATE_CHANGED:
                    if message.src != self._playbin:
                        return

                    _old_state, new_state, _pending = message.parse_state_changed()
                    if new_state == Gst.State.PLAYING:
                        self._is_playing = True
                    elif new_state in (Gst.State.PAUSED, Gst.State.READY, Gst.State.NULL):
                        self._is_playing = False

        try:
            self._run_on_loop(op, allow_after_shutdown=True)
        except Exception:
            pass

    def _advance_to_next_locked(self) -> None:
        if not self._queue:
            self._stop_locked(clear_queue=False)
            return

        next_item = self._queue.popleft()
        self._start_item_locked(next_item)

    def _start_item_locked(self, item: QueuedTrack) -> None:
        track_path = self._find_track_path(item.track_id)
        if track_path is None:
            raise FileNotFoundError(f"Could not find audio file for track id {item.track_id}")

        self._current_item = item
        self._seek_pending = True

        uri = track_path.resolve().as_uri()
        self._playbin.set_property("uri", uri)
        self._playbin.set_property("volume", self._volume)

        result = self._playbin.set_state(Gst.State.PAUSED)
        self._raise_on_state_change_failure(result, "prepare track")

        change_return, _state, _pending = self._playbin.get_state(5 * Gst.SECOND)
        if change_return == Gst.StateChangeReturn.FAILURE:
            raise RuntimeError(f"Failed to load track {item.track_id}")

        self._seek_to_current_start_locked()

        result = self._playbin.set_state(Gst.State.PLAYING)
        self._raise_on_state_change_failure(result, "start playback")
        self._is_playing = True

    def _seek_to_current_start_locked(self) -> None:
        if self._current_item is None:
            return

        start_ns = int(self._current_item.start_second * Gst.SECOND)
        success = self._playbin.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            start_ns,
        )
        if not success:
            raise RuntimeError(
                f"Failed to seek to start_second={self._current_item.start_second} "
                f"for track_id={self._current_item.track_id}"
            )

    def _stop_locked(self, *, clear_queue: bool) -> None:
        self._playbin.set_state(Gst.State.NULL)
        self._current_item = None
        self._seek_pending = False
        self._is_playing = False
        if clear_queue:
            self._queue.clear()

    def _query_position_seconds(self) -> Optional[float]:
        success, position_ns = self._playbin.query_position(Gst.Format.TIME)
        if not success or position_ns < 0:
            return None
        return float(position_ns) / float(Gst.SECOND)

    def _find_track_path(self, track_id: int) -> Optional[Path]:
        exact_prefix = f"{track_id}"
        candidates = sorted(self._track_data_dir.glob(f"{exact_prefix}.*"))
        if candidates:
            return candidates[0]

        for extension in self._common_audio_extensions():
            candidate = self._track_data_dir / f"{track_id}{extension}"
            if candidate.exists():
                return candidate

        return None

    @staticmethod
    def _common_audio_extensions() -> tuple[str, ...]:
        mime_types = (
            "audio/mpeg",
            "audio/mp3",
            "audio/wav",
            "audio/x-wav",
            "audio/flac",
            "audio/ogg",
            "audio/x-m4a",
            "audio/aac",
            "audio/mp4",
            "audio/webm",
            "application/ogg",
        )

        extensions: list[str] = []
        for mime_type in mime_types:
            extension = mimetypes.guess_extension(mime_type)
            if extension is not None and extension not in extensions:
                extensions.append(extension)

        return tuple(extensions)

    @staticmethod
    def _raise_on_state_change_failure(
        result: Gst.StateChangeReturn,
        action: str,
    ) -> None:
        if result == Gst.StateChangeReturn.FAILURE:
            raise RuntimeError(f"GStreamer failed to {action}")