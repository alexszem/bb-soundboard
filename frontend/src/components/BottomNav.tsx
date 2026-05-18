import { Button, Paper } from '@mantine/core';
export type Page = 'main' | 'snippets' | 'players' | 'files';
const items: { page: Page; label: string }[] = [
  { page: 'main', label: 'Main' },
  { page: 'snippets', label: 'Snippets' },
  { page: 'players', label: 'Players' },
  { page: 'files', label: 'Files' },
];
export function BottomNav({ active, onChange }: { active: Page; onChange: (page: Page) => void }) {
  return <Paper className="bottom-nav" shadow="md" p="xs">{items.map((item) => <Button key={item.page} fullWidth color={active === item.page ? 'red' : 'gray'} variant={active === item.page ? 'filled' : 'light'} onClick={() => onChange(item.page)}>{item.label}</Button>)}</Paper>;
}
