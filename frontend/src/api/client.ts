import type { AudioFile, AudioFilePage, Player, RandomSnippet, Snippet, SnippetCreateResponse, SnippetPage, SnippetType } from './types';

export const API_BASE_URL = ""

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: options?.body instanceof FormData ? undefined : { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(text || `${response.status} ${response.statusText}`);
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

function optionalNumber(value?: number | null) {
  return typeof value === 'number' && Number.isFinite(value) ? value : null;
}

export function resolveAudioUrl(url: string) {
  if (/^https?:\/\//i.test(url)) return url;
  return `${API_BASE_URL}${url.startsWith('/') ? '' : '/'}${url}`;
}

export const api = {
  listAudioFiles: () => request<AudioFilePage>('/audio-files?limit=500&offset=0'),
  getAudioFile: (id: number) => request<AudioFile>(`/audio-files/${id}`),
  createAudioFile: (input: { file: File; artist?: string; song?: string; comment?: string }) => {
    const form = new FormData();
    form.append('file', input.file);
    if (input.artist) form.append('artist', input.artist);
    if (input.song) form.append('song', input.song);
    if (input.comment) form.append('comment', input.comment);
    return request<AudioFile>('/audio-files', { method: 'POST', body: form });
  },
  deleteAudioFile: (id: number) => request<void>(`/audio-files/${id}`, { method: 'DELETE' }),

  listSnippets: (snippetTypeId?: number) => {
    const params = new URLSearchParams({ limit: '500', offset: '0' });
    if (snippetTypeId) params.set('snippet_type_id', String(snippetTypeId));
    return request<SnippetPage>(`/snippets?${params}`);
  },
  createSnippet: (input: { audio_file_id: number; snippet_type_id: number; start_time?: number | null; end_time?: number | null }) =>
    request<SnippetCreateResponse>('/snippets', {
      method: 'POST',
      body: JSON.stringify({
        audio_file_id: input.audio_file_id,
        snippet_type_id: input.snippet_type_id,
        start_time: optionalNumber(input.start_time),
        end_time: optionalNumber(input.end_time),
      }),
    }),
  deleteSnippet: (id: number) => request<void>(`/snippets/${id}`, { method: 'DELETE' }),

  listSnippetTypes: () => request<SnippetType[]>('/snippet-types'),
  randomSnippet: (snippetTypeId: number) => request<RandomSnippet>(`/snippet-types/${snippetTypeId}/random-snippet`),

  listPlayers: () => request<Player[]>('/players'),
  createPlayer: (name: string, walkup_snippet_id?: number | null) =>
    request<Player>('/players', { method: 'POST', body: JSON.stringify({ name, walkup_snippet_id }) }),
  updatePlayerWalkup: (name: string, walkup_snippet_id: number | null) =>
    request<Player>(`/players/${encodeURIComponent(name)}/walkup-snippet`, {
      method: 'PATCH',
      body: JSON.stringify({ walkup_snippet_id }),
    }),
  deletePlayer: (name: string) => request<void>(`/players/${encodeURIComponent(name)}`, { method: 'DELETE' }),
};
