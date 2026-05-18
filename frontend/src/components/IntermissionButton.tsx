import { Button } from '@mantine/core';
import { api } from '../api/client';
import type { PlaySound } from '../hooks/useAudioPlayer';
import { nowPlayingTitle } from '../utils/labels';
const INTERMISSION_TYPE_ID = 1;
export function IntermissionButton({ play }: { play: PlaySound }) {
  async function playNextIntermission() {
    await play(async () => {
      const snippet = await api.randomSnippet(INTERMISSION_TYPE_ID);
      const file = await api.getAudioFile(snippet.audio_file_id).catch(() => null);
      return { title: nowPlayingTitle(snippet.snippet_type_name, file), url: snippet.url, startTime: snippet.start_time, endTime: snippet.end_time, loopAfterEnd: playNextIntermission };
    });
  }
  return <Button fullWidth size="lg" color="red" onClick={playNextIntermission}>Intermission</Button>;
}
