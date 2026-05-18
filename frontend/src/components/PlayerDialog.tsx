import { Button, Group, Modal, Select, Stack, TextInput } from '@mantine/core';
import { useEffect, useMemo, useState } from 'react';
import { api } from '../api/client';
import type { AudioFile, Player, Snippet } from '../api/types';
import { audioFilePickLabel } from '../utils/labels';

const WALKUP_SNIPPET_TYPE_ID = 2;

export function PlayerDialog({ opened, onClose, player, snippets, audioFiles, onSaved }: {
  opened: boolean;
  onClose: () => void;
  player?: Player | null;
  snippets: Snippet[];
  audioFiles: AudioFile[];
  onSaved: () => void;
}) {
  const [name, setName] = useState('');
  const [audioFileId, setAudioFileId] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const currentWalkupSnippet = useMemo(
    () => snippets.find((snippet) => snippet.id === player?.walkup_snippet_id),
    [player?.walkup_snippet_id, snippets]
  );

  useEffect(() => {
    setName(player?.name ?? '');
    setAudioFileId(currentWalkupSnippet ? String(currentWalkupSnippet.audio_file_id) : null);
  }, [currentWalkupSnippet, player, opened]);

  async function resolveWalkupSnippetId(selectedAudioFileId: number) {
    try {
      const created = await api.createSnippet(selectedAudioFileId, WALKUP_SNIPPET_TYPE_ID);
      return created.id;
    } catch (error) {
      const existing = snippets.find(
        (snippet) => snippet.audio_file_id === selectedAudioFileId && snippet.snippet_type_id === WALKUP_SNIPPET_TYPE_ID
      );
      if (existing) return existing.id;

      const refreshed = await api.listSnippets();
      const refreshedExisting = refreshed.items.find(
        (snippet) => snippet.audio_file_id === selectedAudioFileId && snippet.snippet_type_id === WALKUP_SNIPPET_TYPE_ID
      );
      if (refreshedExisting) return refreshedExisting.id;

      throw error;
    }
  }

  async function save() {
    setSaving(true);
    try {
      const walkupSnippetId = audioFileId ? await resolveWalkupSnippetId(Number(audioFileId)) : null;
      if (player) {
        await api.updatePlayerWalkup(player.name, walkupSnippetId);
      } else {
        await api.createPlayer(name.trim(), walkupSnippetId);
      }
      onSaved();
      onClose();
    } finally {
      setSaving(false);
    }
  }

  async function remove() {
    if (!player) return;
    await api.deletePlayer(player.name);
    onSaved();
    onClose();
  }

  return (
    <Modal opened={opened} onClose={onClose} title={player ? 'Edit player' : 'Add player'} centered>
      <Stack>
        <TextInput label="Name" value={name} onChange={(e) => setName(e.currentTarget.value)} disabled={!!player} />
        <Select
          label="Walkup audio file"
          placeholder="No walkup"
          value={audioFileId}
          onChange={setAudioFileId}
          clearable
          searchable
          data={audioFiles.map((file) => ({
            value: String(file.id),
            label: audioFilePickLabel(file),
          }))}
        />
        <Group grow>
          {player && <Button color="gray" variant="light" onClick={remove}>Delete</Button>}
          <Button color="red" loading={saving} disabled={!player && !name.trim()} onClick={save}>Save</Button>
        </Group>
      </Stack>
    </Modal>
  );
}
