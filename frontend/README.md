# Soundboard Mobile Client

```bash
bun install
cp .env.example .env
bun run dev
```

Set `VITE_API_BASE_URL` to your backend URL.

Supports snippet `start_time` and `end_time`; playback stops at `end_time` and starts at `start_time` when provided.
