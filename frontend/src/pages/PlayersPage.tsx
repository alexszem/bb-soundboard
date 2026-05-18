import { Button, Card, Stack, Text } from '@mantine/core';
import { useState } from 'react';
import type { Player, Snippet } from '../api/types';
import { Fab } from '../components/Fab';
import { PlayerDialog } from '../components/PlayerDialog';

export function PlayersPage({ players, snippets, reload }: {
  players: Player[];
  snippets: Snippet[];
  reload: () => void;
}) {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);

  function openPlayer(player: Player) {
    setSelectedPlayer(player);
    setDialogOpen(true);
  }

  function openNew() {
    setSelectedPlayer(null);
    setDialogOpen(true);
  }

  return (
    <>
      <Text fw={800} size="lg" mb="xs">Players</Text>
      <Stack gap="xs">
        {players.map((player) => (
          <Card key={player.name} withBorder radius="md" p="sm">
            <Button fullWidth justify="space-between" color="red" variant="subtle" onClick={() => openPlayer(player)}>
              {player.name}
            </Button>
          </Card>
        ))}
        {players.length === 0 && <Text c="dimmed">No players yet.</Text>}
      </Stack>
      <Fab onClick={openNew} />
      <PlayerDialog
        opened={dialogOpen}
        onClose={() => setDialogOpen(false)}
        player={selectedPlayer}
        snippets={snippets}
        onSaved={reload}
      />
    </>
  );
}
