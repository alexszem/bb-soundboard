import { Button, Card, Group, Modal, Stack, Text } from '@mantine/core';
import { useMemo, useState } from 'react';
import { api } from '../api/client';
import type { AudioFile, Snippet, SnippetType } from '../api/types';
import { snippetLabel } from '../utils/labels';

export function DeleteSnippetsDialog({ opened, onClose, type, snippets, audioFiles, onSaved }: {
  opened: boolean;
  onClose: () => void;
  type: SnippetType | null;
  snippets: Snippet[];
  audioFiles: AudioFile[];
  onSaved: () => void;
}) {
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const typeSnippets = useMemo(
    () => snippets.filter((snippet) => snippet.snippet_type_id === type?.id),
    [snippets, type],
  );

  async function remove(id: number) {
    setDeletingId(id);
    try {
      await api.deleteSnippet(id);
      onSaved();
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <Modal opened={opened} onClose={onClose} title={type ? `Delete ${type.name} snippets` : 'Delete snippets'} centered>
      <Stack gap="xs">
        {typeSnippets.length === 0 && <Text c="dimmed">No snippets for this type.</Text>}
        {typeSnippets.map((snippet) => (
          <Card key={snippet.id} withBorder radius="md" p="sm">
            <Group justify="space-between" align="start" wrap="nowrap">
              <div>
                <Text fw={700}>{snippetLabel(snippet, audioFiles)}</Text>
                <Text size="xs" c="dimmed">Snippet #{snippet.id}</Text>
              </div>
              <Button
                color="gray"
                variant="light"
                size="xs"
                loading={deletingId === snippet.id}
                onClick={() => remove(snippet.id)}
              >
                Delete
              </Button>
            </Group>
          </Card>
        ))}
      </Stack>
    </Modal>
  );
}
