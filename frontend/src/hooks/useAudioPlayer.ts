import { useCallback, useEffect, useRef, useState } from 'react';
import { resolveAudioUrl } from '../api/client';

export type PlayingInfo = {
  title: string;
  url: string;
  loopAfterEnd?: () => Promise<void> | void;
};

export function useAudioPlayer() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const stopRequestedRef = useRef(false);
  const [playing, setPlaying] = useState<PlayingInfo | null>(null);

  const stop = useCallback(() => {
    stopRequestedRef.current = true;
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current.src = '';
      audioRef.current = null;
    }
    setPlaying(null);
  }, []);

  const play = useCallback(
    async (info: PlayingInfo) => {
      stop();
      stopRequestedRef.current = false;

      const audio = new Audio(resolveAudioUrl(info.url));
      audioRef.current = audio;
      setPlaying(info);

      audio.onended = async () => {
        audioRef.current = null;
        setPlaying(null);
        if (!stopRequestedRef.current && info.loopAfterEnd) {
          await info.loopAfterEnd();
        }
      };

      audio.onerror = () => {
        audioRef.current = null;
        setPlaying(null);
      };

      await audio.play();
    },
    [stop]
  );

  useEffect(() => stop, [stop]);

  return { playing, play, stop };
}
