// src/services/api.ts
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/docs#"; // URL local de FastAPI

export const chat = async (userId: string, message: string) => {
  const response = await axios.post(`${API_URL}/chat/stream`, { user_id: userId, message });
  return response.data;
};

export const chatStream = async (
  userId: string,
  message: string,
  onChunk: (chunk: string) => void
) => {
  const response = await fetch("http://localhost:8000/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      message
    })
  });

  if (!response.ok) {
    throw new Error("Error en la conexión con el backend");
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) return;

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    onChunk(decoder.decode(value));
  }
};
