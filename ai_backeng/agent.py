import google.generativeai as genai
import os
from dotenv import load_dotenv
from ai_backeng.prompt import SYSTEM_PROMPT

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=API_KEY)

def run_agent(user_message, profile, careers):
    career_text = "\n".join([
        f"- {c['career_name']}: {c['description']}"
        for c in careers
    ])

    full_prompt = f"""
{SYSTEM_PROMPT}

============================
MENSAJE DEL USUARIO
============================
{user_message}

============================
PERFIL ACTUAL (MEMORIA)
============================
{profile}

============================
CARRERAS DISPONIBLES
============================
{career_text}
"""

    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config={"temperature": 0.4}
    )

    try:
        response = model.generate_content(full_prompt)

        # Manejo seguro de la respuesta
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]

            # Acceso directo al texto
            if hasattr(candidate, "content") and hasattr(candidate.content, "text"):
                return candidate.content.text

        return "Error en Gemini: no se generó texto"
    except Exception as e:
        return f"Error en Gemini: {str(e)}"
