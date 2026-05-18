import { useCallback, useEffect, useRef, useState } from 'react';
import { resolveAudioUrl } from '../api/client';

export type PlayingInfo = {
  title: string;
  url: string;
  loopAfterEnd?: () => Promise<void> | void;
};

export type PlayInput = PlayingInfo | (() => PlayingInfo | Promise<PlayingInfo>);
export type PlaySound = (input: PlayInput) => Promise<void>;

function cleanupAudio(audio: HTMLAudioElement) {
  audio.onended = null;
  audio.onerror = null;
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

  const play = useCallback(async (input: PlayInput) => {
    const playId = playIdRef.current + 1;
    playIdRef.current = playId;
    stopRequestedRef.current = false;

    if (audioRef.current) {
      cleanupAudio(audioRef.current);
      audioRef.current = null;
    }

    const inputIsLoader = typeof input === 'function';
    if (inputIsLoader) {
      setPlaying({ title: 'Loading sound…', url: '' });
    }

    let info: PlayingInfo;
    try {
      info = inputIsLoader ? await input() : input;
    } catch (error) {
      if (playIdRef.current === playId) {
        setPlaying(null);
      }
      console.error(error);
      return;
    }

    if (playIdRef.current !== playId || stopRequestedRef.current) {
      return;
    }

    const audio = new Audio(resolveAudioUrl(info.url));
    audioRef.current = audio;
    setPlaying(info);

    audio.onended = async () => {
      if (playIdRef.current !== playId || audioRef.current !== audio) return;

      audioRef.current = null;
      setPlaying(null);

      if (!stopRequestedRef.current && info.loopAfterEnd) {
        await info.loopAfterEnd();
      }
    };

    audio.onerror = () => {
      if (playIdRef.current !== playId || audioRef.current !== audio) return;

      audioRef.current = null;
      setPlaying(null);
    };

    try {
      await audio.play();
    } catch (error) {
      if (playIdRef.current !== playId || audioRef.current !== audio) return;

      audioRef.current = null;
      setPlaying(null);
      console.error(error);
    }
  }, []);

  useEffect(() => stop, [stop]);

  return { playing, play, stop };
}
