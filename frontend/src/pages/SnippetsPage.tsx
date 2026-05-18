import { Button, Card, Group, Stack, Text } from '@mantine/core';
import { useState } from 'react';
import type { AudioFile, Snippet, SnippetType } from '../api/types';
import { AddSnippetDialog } from '../components/AddSnippetDialog';
import { DeleteSnippetsDialog } from '../components/DeleteSnippetsDialog';
import { Fab } from '../components/Fab';

function isHidden(type: SnippetType) {
  return (type.category ?? '').trim().toLowerCase() === 'hidden';
}

export function SnippetsPage({ audioFiles, snippetTypes, snippets, reload }: {
  audioFiles: AudioFile[];
  snippetTypes: SnippetType[];
  snippets: Snippet[];
  reload: () => void;
}) {
  const [addOpen, setAddOpen] = useState(false);
  const [selectedType, setSelectedType] = useState<SnippetType | null>(null);

  const visibleTypes = snippetTypes.filter((type) => !isHidden(type));
  const byCategory = visibleTypes.reduce<Record<string, SnippetType[]>>((acc, type) => {
    const category = type.category || 'Other';
    acc[category] ??= [];
    acc[category].push(type);
    return acc;
  }, {});

  return (
    <>
      <Text fw={800} size="lg" mb="xs">Snippets</Text>
      <Text size="sm" c="dimmed" mb="md">Tap a type to manage and delete its snippets.</Text>
      <Stack gap="sm">
        {Object.entries(byCategory).map(([category, types]) => (
          <Card key={category} withBorder radius="md">
            <Text fw={700} mb="xs">{category}</Text>
            <Group gap="xs">
              {types.map((type) => (
                <Button key={type.id} color="red" variant="light" onClick={() => setSelectedType(type)}>
                  {type.name}
                </Button>
              ))}
            </Group>
          </Card>
        ))}
        {visibleTypes.length === 0 && <Text c="dimmed">No snippet types yet.</Text>}
      </Stack>
      <Fab onClick={() => setAddOpen(true)} />
      <AddSnippetDialog
        opened={addOpen}
        onClose={() => setAddOpen(false)}
        audioFiles={audioFiles}
        snippetTypes={snippetTypes}
        onSaved={reload}
      />
      <DeleteSnippetsDialog
        opened={!!selectedType}
        onClose={() => setSelectedType(null)}
        type={selectedType}
        snippets={snippets}
        audioFiles={audioFiles}
        onSaved={reload}
      />
    </>
  );
}
