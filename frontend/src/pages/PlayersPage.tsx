import { Button, Card, Stack, Text } from '@mantine/core';
import { useState } from 'react';
import type { AudioFile, Player, Snippet } from '../api/types';
import { Fab } from '../components/Fab';
import { PlayerDialog } from '../components/PlayerDialog';
import { audioFileTitle, timeRangeLabel } from '../utils/labels';
export function PlayersPage({ players, snippets, audioFiles, reload }: { players: Player[]; snippets: Snippet[]; audioFiles: AudioFile[]; reload: () => void }) {
  const [dialogOpen, setDialogOpen] = useState(false); const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  function openPlayer(player: Player) { setSelectedPlayer(player); setDialogOpen(true); }
  function openNew() { setSelectedPlayer(null); setDialogOpen(true); }
  function walkupTitle(player: Player) { const snippet = snippets.find((item) => item.id === player.walkup_snippet_id); const file = audioFiles.find((item) => item.id === snippet?.audio_file_id); return file ? `${audioFileTitle(file)} · ${timeRangeLabel(snippet?.start_time, snippet?.end_time)}` : 'No walkup song'; }
  return <><Text fw={800} size="lg" mb="xs">Players</Text><Stack gap="xs">{players.map((player) => <Card key={player.name} withBorder radius="md" p="sm"><Button fullWidth color="red" variant="subtle" className="player-card-button" onClick={() => openPlayer(player)}><span>{player.name}</span><small>{walkupTitle(player)}</small></Button></Card>)}{players.length === 0 && <Text c="dimmed">No players yet.</Text>}</Stack><Fab onClick={openNew} /><PlayerDialog opened={dialogOpen} onClose={() => setDialogOpen(false)} player={selectedPlayer} snippets={snippets} audioFiles={audioFiles} onSaved={reload} /></>;
}
