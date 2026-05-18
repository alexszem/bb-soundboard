import { useCallback, useEffect, useRef, useState } from 'react';
import { resolveAudioUrl } from '../api/client';

export type PlayingInfo = {
  title: string;
  url: string;
  startTime?: number | null;
  endTime?: number | null;
  loopAfterEnd?: () => Promise<void> | void;
};

export type PlayInput = PlayingInfo | (() => PlayingInfo | Promise<PlayingInfo>);
export type PlaySound = (input: PlayInput) => Promise<void>;

function validTime(value?: number | null) {
  return typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null;
}

function cleanupAudio(audio: HTMLAudioElement) {
  audio.onended = null;
  audio.onerror = null;
  audio.ontimeupdate = null;
  audio.onloadedmetadata = null;
  audio.pause();
  audio.currentTime = 0;
  audio.removeAttribute('src');
  audio.load();
}

export function useAudioPlayer() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const playIdRef = useRef(0);
  const stopRequestedRef = useRef(false);
  const [playing, setPlaying] = useState<PlayingInfo | null>(null);

  const stop = useCallback(() => {
    playIdRef.current += 1;
    stopRequestedRef.current = true;
    if (audioRef.current) {
      cleanupAudio(audioRef.current);
      audioRef.current = null;
    }
    setPlaying(null);
  }, []);

  const finishCurrent = useCallback(async (playId: number, audio: HTMLAudioElement, info: PlayingInfo) => {
    if (playIdRef.current !== playId || audioRef.current !== audio) return;
    audioRef.current = null;
    cleanupAudio(audio);
    setPlaying(null);
    if (!stopRequestedRef.current && info.loopAfterEnd) await info.loopAfterEnd();
  }, []);

  const play = useCallback(async (input: PlayInput) => {
    const playId = playIdRef.current + 1;
    playIdRef.current = playId;
    stopRequestedRef.current = false;

    if (audioRef.current) {
      cleanupAudio(audioRef.current);
      audioRef.current = null;
    }

    const inputIsLoader = typeof input === 'function';
    if (inputIsLoader) setPlaying({ title: 'Loading sound…', url: '' });

    let info: PlayingInfo;
    try {
      info = inputIsLoader ? await input() : input;
    } catch (error) {
      if (playIdRef.current === playId) setPlaying(null);
      console.error(error);
      return;
    }

    if (playIdRef.current !== playId || stopRequestedRef.current) return;

    const startTime = validTime(info.startTime);
    const endTime = validTime(info.endTime);
    const audio = new Audio(resolveAudioUrl(info.url));
    audioRef.current = audio;
    setPlaying({ ...info, startTime, endTime });

    let didSeekToStart = false;
    const seekToStart = () => {
      if (didSeekToStart || startTime === null) return;
      try {
        audio.currentTime = startTime;
        didSeekToStart = true;
      } catch {
        // Some browsers only allow seeking after metadata is available.
      }
    };

    audio.onloadedmetadata = seekToStart;
    audio.ontimeupdate = () => {
      if (playIdRef.current !== playId || audioRef.current !== audio) return;
      if (endTime !== null && audio.currentTime >= endTime) {
        void finishCurrent(playId, audio, info);
      }
    };
    audio.onended = () => { void finishCurrent(playId, audio, info); };
    audio.onerror = () => {
      if (playIdRef.current !== playId || audioRef.current !== audio) return;
      audioRef.current = null;
      setPlaying(null);
    };

    try {
      seekToStart();
      await audio.play();
    } catch (error) {
      if (playIdRef.current !== playId || audioRef.current !== audio) return;
      audioRef.current = null;
      setPlaying(null);
      console.error(error);
    }
  }, [finishCurrent]);

  useEffect(() => stop, [stop]);
  return { playing, play, stop };
}
