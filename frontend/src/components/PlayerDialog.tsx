import { Button, Group, Modal, NumberInput, Select, Stack, Text, TextInput } from '@mantine/core';
import { useEffect, useMemo, useState } from 'react';
import { api } from '../api/client';
import type { AudioFile, Player, Snippet } from '../api/types';
import { audioFilePickLabel, timeRangeLabel } from '../utils/labels';
const WALKUP_SNIPPET_TYPE_ID = 2;
function optionalSeconds(value: string | number) { if (value === '') return null; const parsed = Number(value); return Number.isFinite(parsed) && parsed >= 0 ? parsed : null; }
function sameOptionalNumber(a?: number | null, b?: number | null) { return (a ?? null) === (b ?? null); }
export function PlayerDialog({ opened, onClose, player, snippets, audioFiles, onSaved }: { opened: boolean; onClose: () => void; player?: Player | null; snippets: Snippet[]; audioFiles: AudioFile[]; onSaved: () => void }) {
  const [name, setName] = useState('');
  const [audioFileId, setAudioFileId] = useState<string | null>(null);
  const [startTime, setStartTime] = useState<string | number>('');
  const [endTime, setEndTime] = useState<string | number>('');
  const [saving, setSaving] = useState(false);
  const currentWalkupSnippet = useMemo(() => snippets.find((snippet) => snippet.id === player?.walkup_snippet_id), [player?.walkup_snippet_id, snippets]);
  useEffect(() => {
    setName(player?.name ?? '');
    setAudioFileId(currentWalkupSnippet ? String(currentWalkupSnippet.audio_file_id) : null);
    setStartTime(currentWalkupSnippet?.start_time ?? '');
    setEndTime(currentWalkupSnippet?.end_time ?? '');
  }, [currentWalkupSnippet, player, opened]);
  async function resolveWalkupSnippetId(selectedAudioFileId: number, selectedStartTime: number | null, selectedEndTime: number | null) {
    try {
      const created = await api.createSnippet({ audio_file_id: selectedAudioFileId, snippet_type_id: WALKUP_SNIPPET_TYPE_ID, start_time: selectedStartTime, end_time: selectedEndTime });
      return created.id;
    } catch (error) {
      const byAudioAndType = (snippet: Snippet) => snippet.audio_file_id === selectedAudioFileId && snippet.snippet_type_id === WALKUP_SNIPPET_TYPE_ID;
      const exactExisting = snippets.find((snippet) => byAudioAndType(snippet) && sameOptionalNumber(snippet.start_time, selectedStartTime) && sameOptionalNumber(snippet.end_time, selectedEndTime));
      if (exactExisting) return exactExisting.id;
      const anyExisting = snippets.find(byAudioAndType);
      if (anyExisting) return anyExisting.id;
      const refreshed = await api.listSnippets(WALKUP_SNIPPET_TYPE_ID);
      const refreshedExact = refreshed.items.find((snippet) => byAudioAndType(snippet) && sameOptionalNumber(snippet.start_time, selectedStartTime) && sameOptionalNumber(snippet.end_time, selectedEndTime));
      if (refreshedExact) return refreshedExact.id;
      const refreshedAny = refreshed.items.find(byAudioAndType);
      if (refreshedAny) return refreshedAny.id;
      throw error;
    }
  }
  async function save() {
    setSaving(true);
    try {
      const selectedStartTime = optionalSeconds(startTime);
      const selectedEndTime = optionalSeconds(endTime);
      const walkupSnippetId = audioFileId ? await resolveWalkupSnippetId(Number(audioFileId), selectedStartTime, selectedEndTime) : null;
      if (player) await api.updatePlayerWalkup(player.name, walkupSnippetId); else await api.createPlayer(name.trim(), walkupSnippetId);
      onSaved(); onClose();
    } finally { setSaving(false); }
  }
  async function remove() { if (!player) return; await api.deletePlayer(player.name); onSaved(); onClose(); }
  return <Modal opened={opened} onClose={onClose} title={player ? 'Edit player' : 'Add player'} centered><Stack><TextInput label="Name" value={name} onChange={(e) => setName(e.currentTarget.value)} disabled={!!player} /><Select label="Walkup audio file" placeholder="No walkup" value={audioFileId} onChange={setAudioFileId} clearable searchable data={audioFiles.map((file) => ({ value: String(file.id), label: audioFilePickLabel(file) }))} /><Group grow><NumberInput label="Start time (s)" placeholder="Full start" min={0} decimalScale={3} value={startTime} onChange={setStartTime} /><NumberInput label="End time (s)" placeholder="Full end" min={0} decimalScale={3} value={endTime} onChange={setEndTime} /></Group><Text size="xs" c="dimmed">When a walkup snippet already exists for this audio file, the app reuses it. Without a snippet update route, existing server-side times cannot be changed here. Current range: {timeRangeLabel(optionalSeconds(startTime), optionalSeconds(endTime))}</Text><Group grow>{player && <Button color="gray" variant="light" onClick={remove}>Delete</Button>}<Button color="red" loading={saving} disabled={!player && !name.trim()} onClick={save}>Save</Button></Group></Stack></Modal>;
}
