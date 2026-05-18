import { Button, FileInput, Group, Modal, Stack, TextInput } from '@mantine/core';
import { useState } from 'react';
import { api } from '../api/client';

export function AudioFileDialog({ opened, onClose, onSaved }: {
  opened: boolean;
  onClose: () => void;
  onSaved: () => void;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [artist, setArtist] = useState('');
  const [song, setSong] = useState('');
  const [comment, setComment] = useState('');
  const [saving, setSaving] = useState(false);

  async function save() {
    if (!file) return;
    setSaving(true);
    try {
      await api.createAudioFile({ file, artist, song, comment });
      setFile(null);
      setArtist('');
      setSong('');
      setComment('');
      onSaved();
      onClose();
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal opened={opened} onClose={onClose} title="Add sound file" centered>
      <Stack>
        <FileInput label="Audio file" placeholder="Pick a file" accept="audio/*" value={file} onChange={setFile} />
        <TextInput label="Artist" value={artist} onChange={(e) => setArtist(e.currentTarget.value)} />
        <TextInput label="Song" value={song} onChange={(e) => setSong(e.currentTarget.value)} />
        <TextInput label="Comment" value={comment} onChange={(e) => setComment(e.currentTarget.value)} />
        <Group grow>
          <Button color="gray" variant="light" onClick={onClose}>Cancel</Button>
          <Button color="red" loading={saving} disabled={!file} onClick={save}>Upload</Button>
        </Group>
      </Stack>
    </Modal>
  );
}
