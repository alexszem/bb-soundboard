import { Button, Card, Group, Stack, Text } from '@mantine/core';
import { useState } from 'react';
import { api } from '../api/client';
import type { AudioFile } from '../api/types';
import { AudioFileDialog } from '../components/AudioFileDialog';
import { Fab } from '../components/Fab';

export function FilesPage({ audioFiles, reload }: { audioFiles: AudioFile[]; reload: () => void }) {
  const [dialogOpen, setDialogOpen] = useState(false);

  async function remove(id: number) {
    await api.deleteAudioFile(id);
    reload();
  }

  return (
    <>
      <Text fw={800} size="lg" mb="xs">Sound files</Text>
      <Stack gap="xs">
        {audioFiles.map((file) => (
          <Card key={file.id} withBorder radius="md" p="sm">
            <Group justify="space-between" align="start" wrap="nowrap">
              <div>
                <Text fw={700}>{file.artist ?? 'Unknown artist'} - {file.song ?? `File #${file.id}`}</Text>
                <Text size="xs" c="dimmed">{file.mime_type}{file.comment ? ` · ${file.comment}` : ''}</Text>
              </div>
              <Button color="gray" variant="light" size="xs" onClick={() => remove(file.id)}>Delete</Button>
            </Group>
          </Card>
        ))}
        {audioFiles.length === 0 && <Text c="dimmed">No files uploaded yet.</Text>}
      </Stack>
      <Fab onClick={() => setDialogOpen(true)} />
      <AudioFileDialog opened={dialogOpen} onClose={() => setDialogOpen(false)} onSaved={reload} />
    </>
  );
}
