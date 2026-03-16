import axios from 'axios';
import type { Memo, GenerateResponse, RawInput, ApiListResponse } from '@/types/memo';

const api = axios.create({
  baseURL: 'http://localhost:7070/'
});

export const MemoService = {
  getAll: async (): Promise<Memo[]> => {
    const res = await api.get<ApiListResponse | Memo[]>('/memo/');
    const data = res.data;
    // API returns { data: [...] } wrapper
    if (data && typeof data === 'object' && 'data' in data && Array.isArray((data as ApiListResponse).data)) {
      return (data as ApiListResponse).data;
    }
    return Array.isArray(data) ? data : [];
  },
  getById: async (id: string): Promise<Memo> => {
    const res = await api.get(`/memo/${id}`);
    const data = res.data;
    // Handle wrapped response { data: {...} }
    if (data && typeof data === 'object' && 'data' in data && !('memo_id' in data)) {
      return data.data;
    }
    return data;
  },
  generate: (rawInputs: RawInput[]) =>
    api.post<GenerateResponse>('/memo/generate', { raw_inputs: rawInputs }).then(r => r.data),
  delete: (id: string) => api.delete(`/memo/${id}`).then(r => r.data),
};
