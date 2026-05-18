import { Button, Group, Modal, Select, Stack } from '@mantine/core';
import { useState } from 'react';
import { api } from '../api/client';
import type { AudioFile, SnippetType } from '../api/types';

export function AddSnippetDialog({ opened, onClose, audioFiles, snippetTypes, onSaved }: {
  opened: boolean;
  onClose: () => void;
  audioFiles: AudioFile[];
  snippetTypes: SnippetType[];
  onSaved: () => void;
}) {
  const [audioFileId, setAudioFileId] = useState<string | null>(null);
  const [snippetTypeId, setSnippetTypeId] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function save() {
    if (!audioFileId || !snippetTypeId) return;
    setSaving(true);
    try {
      await api.createSnippet(Number(audioFileId), Number(snippetTypeId));
      setAudioFileId(null);
      setSnippetTypeId(null);
      onSaved();
      onClose();
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal opened={opened} onClose={onClose} title="Add snippet" centered>
      <Stack>
        <Select
          label="Audio file"
          placeholder="Pick file"
          value={audioFileId}
          onChange={setAudioFileId}
          data={audioFiles.map((file) => ({ value: String(file.id), label: `${file.artist ?? 'Unknown'} - ${file.song ?? `File #${file.id}`}` }))}
          searchable
        />
        <Select
          label="Snippet type"
          placeholder="Pick type"
          value={snippetTypeId}
          onChange={setSnippetTypeId}
          data={snippetTypes.map((type) => ({ value: String(type.id), label: `${type.name}${type.category ? ` (${type.category})` : ''}` }))}
          searchable
        />
        <Group grow>
          <Button variant="light" color="gray" onClick={onClose}>Cancel</Button>
          <Button color="red" loading={saving} onClick={save}>Add</Button>
        </Group>
      </Stack>
    </Modal>
  );
}
