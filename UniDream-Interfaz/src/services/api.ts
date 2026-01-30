// src/services/api.ts
import axios from "axios";

export const API_URL = "http://3.144.209.174";// URL local de FastAPI

export const chat = async (userId: string, message: string) => {
  const response = await axios.post(`${API_URL}/chat/stream`, { user_id: userId, message });
  return response.data;
};

export const chatStream = async (userId: string, message: string, onChunk: (chunk: string) => void) => {
  const response = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message })
  });

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  if (!reader) return;

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    onChunk(chunk);
  }
};