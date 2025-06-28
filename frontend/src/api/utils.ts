import axios, { Method } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface ApiRequestOptions {
  method: Method;
  path: string;
  data?: any;
}

export async function apiRequest<T>({ method, path, data }: ApiRequestOptions): Promise<T> {
  const apiUrl = await AsyncStorage.getItem('api_url');
  const url = `${apiUrl}${path}`;

  try {
    const res = await axios({
      method,
      url,
      data,
    });
    return res.data;
  } catch (e) {
    console.log(`API request failed: ${method.toUpperCase()} ${path}`, e);
    throw e;
  }
}