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

export function audioFileDetail(file?: AudioFile | null) {
  if (!file) return '';
  const parts = [file.comment, file.mime_type].filter(Boolean);
  return parts.join(' · ');
}

export function audioFilePickLabel(file: AudioFile) {
  const base = audioFileTitle(file);
  return file.comment ? `${base} · ${file.comment}` : base;
}

export function snippetTypeLabel(type?: SnippetType | null) {
  if (!type) return 'Unknown type';
  return `${type.name}${type.category ? ` (${type.category})` : ''}`;
}

export function snippetLabel(snippet: Snippet, audioFiles: AudioFile[]) {
  const file = audioFiles.find((audioFile) => audioFile.id === snippet.audio_file_id);
  const title = audioFileTitle(file);
  const comment = file?.comment ? ` · ${file.comment}` : '';
  return `${title}${comment}`;
}

export function nowPlayingTitle(typeName: string, file?: AudioFile | null) {
  return `${typeName}: ${file?.song?.trim() || audioFileTitle(file)}`;
}
