// src/services/api.ts
/// <reference types="vite/client" />
// Si existe una variable de entorno en Vercel, usa esa. Si no, usa localhost.
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const chatWithAI = async (message: string) => {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
      throw new Error("Error en la respuesta del servidor");
    }

    const data = await response.json();
    return data.reply; // Retorna solo el texto de la respuesta
  } catch (error) {
    console.error("Error conectando con el backend:", error);
    return "Lo siento, hubo un error de conexión con el servidor.";
  }
};