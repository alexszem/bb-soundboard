import { Button } from '@mantine/core';

export function Fab({ label = '+', onClick }: { label?: string; onClick: () => void }) {
  return (
    <Button className="fab" color="red" radius="xl" onClick={onClick} aria-label={label}>
      {label}
    </Button>
  );
}
