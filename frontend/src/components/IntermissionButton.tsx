import { Button } from '@mantine/core';
import { api } from '../api/client';
import type { PlayingInfo } from '../hooks/useAudioPlayer';

const INTERMISSION_TYPE_ID = 1;

export function IntermissionButton({ play }: { play: (info: PlayingInfo) => Promise<void> }) {
  async function playNextIntermission() {
    const snippet = await api.randomSnippet(INTERMISSION_TYPE_ID);
    await play({
      title: `Intermission: ${snippet.snippet_type_name}`,
      url: snippet.url,
      loopAfterEnd: playNextIntermission,
    });
  }

  return (
    <Button fullWidth size="lg" color="red" onClick={playNextIntermission}>
      Intermission
    </Button>
  );
}
