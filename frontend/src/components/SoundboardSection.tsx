import { Button, Card, Group, Stack, Text } from '@mantine/core';
import { api } from '../api/client';
import type { SnippetType } from '../api/types';
import type { PlaySound } from '../hooks/useAudioPlayer';

function isHidden(type: SnippetType) {
  return (type.category ?? '').trim().toLowerCase() === 'hidden';
}

export function SoundboardSection({ snippetTypes, play }: {
  snippetTypes: SnippetType[];
  play: PlaySound;
}) {
  const visibleTypes = snippetTypes.filter((type) => !isHidden(type));
  const byCategory = visibleTypes.reduce<Record<string, SnippetType[]>>((acc, type) => {
    const category = type.category || 'Other';
    acc[category] ??= [];
    acc[category].push(type);
    return acc;
  }, {});

  async function playRandom(type: SnippetType) {
    await play(async () => {
      const snippet = await api.randomSnippet(type.id);
      return { title: snippet.snippet_type_name, url: snippet.url };
    });
  }

  return (
    <section>
      <Text fw={800} size="lg" mb="xs">Soundboard</Text>
      <Stack gap="sm">
        {Object.entries(byCategory).map(([category, types]) => (
          <Card key={category} withBorder radius="md">
            <Text fw={700} mb="xs">{category}</Text>
            <Group gap="xs">
              {types.map((type) => (
                <Button key={type.id} color="red" variant="light" onClick={() => playRandom(type)}>
                  {type.name}
                </Button>
              ))}
            </Group>
          </Card>
        ))}
      </Stack>
    </section>
  );
}
