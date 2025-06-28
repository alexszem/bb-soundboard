import AsyncStorage from "@react-native-async-storage/async-storage";
import { apiRequest } from "./utils";
import axios from "axios";

export interface Song {
  id: number;
  name: string;
  artist: string;
  length: number;
}

export interface AddSongResponse {
  message: string;
  song_id: number;
}

export async function getAllSongs(): Promise<Song[]> {
  return await apiRequest<Song[]>({ method: 'GET', path: '/songs' });
}

export async function getSongById(id: number): Promise<Song> {
  return await apiRequest<Song>({ method: 'GET', path: `/songs/${id}` });
}

export async function deleteSong(id: number): Promise<{ message: string }> {
  return await apiRequest<{ message: string }>({ method: 'DELETE', path: `/songs/${id}` });
}

export async function addSong(file: any, name: string, artist: string): Promise<AddSongResponse> {
  const apiUrl = await AsyncStorage.getItem('api_url');
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);
  formData.append('artist', artist);

  try {
    const res = await axios.post(`${apiUrl}/songs/add`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  } catch (e) {
    console.log('API request failed: POST /songs/add', e);
    throw e;
  }
}