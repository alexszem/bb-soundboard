import { Button, Group, Modal, NumberInput, Select, Stack } from '@mantine/core';
import { useState } from 'react';
import { api } from '../api/client';
import type { AudioFile, SnippetType } from '../api/types';
import { audioFilePickLabel, snippetTypeLabel } from '../utils/labels';

function optionalSeconds(value: string | number) {
  if (value === '') return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}

export function AddSnippetDialog({ opened, onClose, audioFiles, snippetTypes, onSaved }: {
  opened: boolean;
  onClose: () => void;
  audioFiles: AudioFile[];
  snippetTypes: SnippetType[];
  onSaved: () => void;
}) {
  const [audioFileId, setAudioFileId] = useState<string | null>(null);
  const [snippetTypeId, setSnippetTypeId] = useState<string | null>(null);
  const [startTime, setStartTime] = useState<string | number>('');
  const [endTime, setEndTime] = useState<string | number>('');
  const [saving, setSaving] = useState(false);

  async function save() {
    if (!audioFileId || !snippetTypeId) return;
    setSaving(true);
    try {
      await api.createSnippet({
        audio_file_id: Number(audioFileId),
        snippet_type_id: Number(snippetTypeId),
        start_time: optionalSeconds(startTime),
        end_time: optionalSeconds(endTime),
      });
      setAudioFileId(null);
      setSnippetTypeId(null);
      setStartTime('');
      setEndTime('');
      onSaved();
      onClose();
    } finally { setSaving(false); }
  }

  return (
    <Modal opened={opened} onClose={onClose} title="Add snippet" centered>
      <Stack>
        <Select label="Audio file" placeholder="Pick file" value={audioFileId} onChange={setAudioFileId} data={audioFiles.map((file) => ({ value: String(file.id), label: audioFilePickLabel(file) }))} searchable />
        <Select label="Snippet type" placeholder="Pick type" value={snippetTypeId} onChange={setSnippetTypeId} data={snippetTypes.map((type) => ({ value: String(type.id), label: snippetTypeLabel(type) }))} searchable />
        <Group grow>
          <NumberInput label="Start time (s)" placeholder="Full start" min={0} decimalScale={3} value={startTime} onChange={setStartTime} />
          <NumberInput label="End time (s)" placeholder="Full end" min={0} decimalScale={3} value={endTime} onChange={setEndTime} />
        </Group>
        <Group grow><Button variant="light" color="gray" onClick={onClose}>Cancel</Button><Button color="red" loading={saving} onClick={save}>Add</Button></Group>
      </Stack>
    </Modal>
  );
}
