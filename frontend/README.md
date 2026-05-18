# Soundboard Mobile Client

A small mobile-first Vite + React + Bun client for the Soundboard API.

## Run

```bash
bun install
cp .env.example .env
bun run dev
```

Set `VITE_API_BASE_URL` to the backend origin, for example `http://localhost:8000`.

## Notes

- Mantine is used for simple mobile UI primitives.
- Only one audio snippet plays at a time.
- The bottom now-playing bar stops audio instead of pausing it.
- The main player list is stored in `localStorage`.
