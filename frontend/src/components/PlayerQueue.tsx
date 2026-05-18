import { ActionIcon, Button, Card, Group, Select, Text } from '@mantine/core';
import { useState } from 'react';
import type { AudioFile, Player, Snippet } from '../api/types';
import type { PlaySound } from '../hooks/useAudioPlayer';
import { audioFileTitle, nowPlayingTitle } from '../utils/labels';
export function PlayerQueue({ players, snippets, audioFiles, queue, setQueue, play }: { players: Player[]; snippets: Snippet[]; audioFiles: AudioFile[]; queue: string[]; setQueue: (queue: string[]) => void; play: PlaySound }) {
  const [dragIndex, setDragIndex] = useState<number | null>(null);
  function addPlayer(name: string | null) { if (name) setQueue([...queue, name]); }
  function removeAt(index: number) { setQueue(queue.filter((_, i) => i !== index)); }
  function move(from: number, to: number) { if (from === to) return; const next = [...queue]; const [item] = next.splice(from, 1); next.splice(to, 0, item); setQueue(next); }
  function walkupSnippet(player: Player) { return snippets.find((item) => item.id === player.walkup_snippet_id); }
  function walkupFile(player: Player) { const snippet = walkupSnippet(player); return audioFiles.find((file) => file.id === snippet?.audio_file_id); }
  async function playPlayer(name: string) {
    const player = players.find((p) => p.name === name); if (!player?.walkup_snippet_url) return;
    const snippet = walkupSnippet(player); const file = walkupFile(player);
    await play({ title: nowPlayingTitle(`${player.name} walkup`, file), url: player.walkup_snippet_url, startTime: snippet?.start_time, endTime: snippet?.end_time });
  }
  return <section><Text fw={800} size="lg" mb="xs">Player order</Text><Select placeholder="Add player" data={players.map((p) => ({ value: p.name, label: p.name }))} onChange={addPlayer} searchable clearable /><div className="player-grid">{queue.length === 0 && <Text c="dimmed">No players added yet.</Text>}{queue.map((name, index) => { const player = players.find((p) => p.name === name); const file = player ? walkupFile(player) : null; return <Card key={`${name}-${index}`} withBorder radius="md" p="xs" draggable className={dragIndex === index ? 'dragging-card' : undefined} onDragStart={() => setDragIndex(index)} onDragOver={(event) => event.preventDefault()} onDrop={() => { if (dragIndex !== null) move(dragIndex, index); setDragIndex(null); }} onDragEnd={() => setDragIndex(null)}><Group justify="space-between" wrap="nowrap" gap="xs"><Button variant="subtle" color="red" className="player-button" onClick={() => playPlayer(name)}><span>{index + 1}. {name}</span>{file && <small>{audioFileTitle(file)}</small>}</Button><ActionIcon color="gray" variant="light" onClick={() => removeAt(index)}>×</ActionIcon></Group></Card>; })}</div></section>;
}
