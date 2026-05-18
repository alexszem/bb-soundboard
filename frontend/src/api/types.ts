export type AudioFile = {
  id: number;
  artist?: string | null;
  song?: string | null;
  comment?: string | null;
  mime_type: string;
  file_extension?: string | null;
  url: string;
};

export type AudioFilePage = { items: AudioFile[]; total: number; limit: number; offset: number };

export type SnippetType = { id: number; name: string; category?: string | null };

export type Snippet = {
  id: number;
  audio_file_id: number;
  snippet_type_id: number;
  snippet_type_name: string;
  category?: string | null;
  start_time?: number | null;
  end_time?: number | null;
  url: string;
};

export type SnippetPage = { items: Snippet[]; total: number; limit: number; offset: number };

export type SnippetCreateResponse = {
  id: number;
  audio_file_id: number;
  snippet_type_id: number;
  start_time?: number | null;
  end_time?: number | null;
};

export type RandomSnippet = {
  snippet_id: number;
  snippet_type_id: number;
  snippet_type_name: string;
  category?: string | null;
  audio_file_id: number;
  start_time?: number | null;
  end_time?: number | null;
  url: string;
};

export type Player = {
  name: string;
  walkup_snippet_id?: number | null;
  walkup_snippet_url?: string | null;
};
