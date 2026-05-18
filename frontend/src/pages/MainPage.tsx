import { Stack } from '@mantine/core';
import type { AudioFile, Player, Snippet, SnippetType } from '../api/types';
import { IntermissionButton } from '../components/IntermissionButton';
import { PlayerQueue } from '../components/PlayerQueue';
import { SoundboardSection } from '../components/SoundboardSection';
import type { PlaySound } from '../hooks/useAudioPlayer';

export function MainPage({ players, snippets, audioFiles, queue, setQueue, snippetTypes, play }: {
  players: Player[];
  snippets: Snippet[];
  audioFiles: AudioFile[];
  queue: string[];
  setQueue: (queue: string[]) => void;
  snippetTypes: SnippetType[];
  play: PlaySound;
}) {
  return (
    <Stack gap="xl">
      <PlayerQueue players={players} snippets={snippets} audioFiles={audioFiles} queue={queue} setQueue={setQueue} play={play} />
      <IntermissionButton play={play} />
      <SoundboardSection snippetTypes={snippetTypes} play={play} />
    </Stack>
  );
}
