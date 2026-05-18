import { Button, Group, Modal, Select, Stack, TextInput } from '@mantine/core';
import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Player, Snippet } from '../api/types';

export function PlayerDialog({ opened, onClose, player, snippets, onSaved }: {
  opened: boolean;
  onClose: () => void;
  player?: Player | null;
  snippets: Snippet[];
  onSaved: () => void;
}) {
  const [name, setName] = useState('');
  const [snippetId, setSnippetId] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setName(player?.name ?? '');
    setSnippetId(player?.walkup_snippet_id ? String(player.walkup_snippet_id) : null);
  }, [player, opened]);

  async function save() {
    setSaving(true);
    try {
      if (player) {
        await api.updatePlayerWalkup(player.name, snippetId ? Number(snippetId) : null);
      } else {
        await api.createPlayer(name.trim(), snippetId ? Number(snippetId) : null);
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
          label="Walkup snippet"
          placeholder="No walkup"
          value={snippetId}
          onChange={setSnippetId}
          clearable
          searchable
          data={snippets.map((snippet) => ({
            value: String(snippet.id),
            label: `#${snippet.id} - ${snippet.snippet_type_name}`,
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
