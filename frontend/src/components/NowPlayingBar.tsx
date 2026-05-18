import { Button, Paper, Text } from '@mantine/core';
import type { PlayingInfo } from '../hooks/useAudioPlayer';
import { timeRangeLabel } from '../utils/labels';

export function NowPlayingBar({ playing, onStop }: { playing: PlayingInfo | null; onStop: () => void }) {
  if (!playing) return null;
  return (
    <Paper className="now-playing" shadow="md" p="sm" radius="md">
      <div>
        <Text size="xs" c="dimmed">Now playing</Text>
        <Text fw={700} lineClamp={1}>{playing.title}</Text>
        {(playing.startTime != null || playing.endTime != null) && <Text size="xs" c="dimmed">{timeRangeLabel(playing.startTime, playing.endTime)}</Text>}
      </div>
      <Button color="red" onClick={onStop}>Stop</Button>
    </Paper>
  );
}
