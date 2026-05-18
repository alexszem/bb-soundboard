import type { AudioFile, Snippet, SnippetType } from '../api/types';

export function audioFileTitle(file?: AudioFile | null) {
  if (!file) return 'Unknown file';
  const artist = file.artist?.trim();
  const song = file.song?.trim();
  if (artist && song) return `${artist} - ${song}`;
  if (song) return song;
  if (artist) return artist;
  return `File #${file.id}`;
}

export function audioFilePickLabel(file: AudioFile) {
  const base = audioFileTitle(file);
  return file.comment ? `${base} · ${file.comment}` : base;
}

export function snippetTypeLabel(type?: SnippetType | null) {
  if (!type) return 'Unknown type';
  return `${type.name}${type.category ? ` (${type.category})` : ''}`;
}

export function timeRangeLabel(start?: number | null, end?: number | null) {
  if (start == null && end == null) return 'Full audio';
  const from = start == null ? 'start' : `${start}s`;
  const to = end == null ? 'end' : `${end}s`;
  return `${from} → ${to}`;
}

export function snippetLabel(snippet: Snippet, audioFiles: AudioFile[]) {
  const file = audioFiles.find((audioFile) => audioFile.id === snippet.audio_file_id);
  const title = audioFileTitle(file);
  const comment = file?.comment ? ` · ${file.comment}` : '';
  return `${title}${comment} · ${timeRangeLabel(snippet.start_time, snippet.end_time)}`;
}

export function nowPlayingTitle(typeName: string, file?: AudioFile | null) {
  return `${typeName}: ${file?.song?.trim() || audioFileTitle(file)}`;
}

export function parseOptionalSeconds(value: string) {
  if (!value.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}
