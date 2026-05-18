import { Stack } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import type { AudioFile, Player, SnippetType } from '../api/types';
import { AddSnippetDialog } from '../components/AddSnippetDialog';
import { Fab } from '../components/Fab';
import { IntermissionButton } from '../components/IntermissionButton';
import { PlayerQueue } from '../components/PlayerQueue';
import { SoundboardSection } from '../components/SoundboardSection';
import type { PlayingInfo } from '../hooks/useAudioPlayer';

export function MainPage({ players, queue, setQueue, snippetTypes, audioFiles, play, reload }: {
  players: Player[];
  queue: string[];
  setQueue: (queue: string[]) => void;
  snippetTypes: SnippetType[];
  audioFiles: AudioFile[];
  play: (info: PlayingInfo) => Promise<void>;
  reload: () => void;
}) {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Stack gap="xl">
        <PlayerQueue players={players} queue={queue} setQueue={setQueue} play={play} />
        <IntermissionButton play={play} />
        <SoundboardSection snippetTypes={snippetTypes} play={play} />
      </Stack>
      <Fab onClick={open} />
      <AddSnippetDialog opened={opened} onClose={close} audioFiles={audioFiles} snippetTypes={snippetTypes} onSaved={reload} />
    </>
  );
}
