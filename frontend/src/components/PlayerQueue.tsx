import { ActionIcon, Button, Card, Group, Select, Stack, Text } from '@mantine/core';
import type { Player } from '../api/types';
import type { PlayingInfo } from '../hooks/useAudioPlayer';

export function PlayerQueue({ players, queue, setQueue, play }: {
  players: Player[];
  queue: string[];
  setQueue: (queue: string[]) => void;
  play: (info: PlayingInfo) => Promise<void>;
}) {
  function addPlayer(name: string | null) {
    if (!name) return;
    setQueue([...queue, name]);
  }

  function removeAt(index: number) {
    setQueue(queue.filter((_, i) => i !== index));
  }

  async function playPlayer(name: string) {
    const player = players.find((p) => p.name === name);
    if (!player?.walkup_snippet_url) return;
    await play({ title: `${player.name} walkup`, url: player.walkup_snippet_url });
  }

  return (
    <section>
      <Text fw={800} size="lg" mb="xs">Player order</Text>
      <Select
        placeholder="Add player"
        data={players.map((p) => ({ value: p.name, label: p.name }))}
        onChange={addPlayer}
        searchable
        clearable
      />
      <Stack mt="sm" gap="xs">
        {queue.length === 0 && <Text c="dimmed">No players added yet.</Text>}
        {queue.map((name, index) => (
          <Card key={`${name}-${index}`} withBorder radius="md" p="sm">
            <Group justify="space-between" wrap="nowrap">
              <Button variant="subtle" color="red" onClick={() => playPlayer(name)}>{index + 1}. {name}</Button>
              <ActionIcon color="gray" variant="light" onClick={() => removeAt(index)}>×</ActionIcon>
            </Group>
          </Card>
        ))}
      </Stack>
    </section>
  );
}
