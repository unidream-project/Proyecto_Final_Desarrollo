import google.generativeai as genai
import os
from dotenv import load_dotenv
from ai_backeng.prompt import SYSTEM_PROMPT

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config={
            "temperature": 0.4,
            "max_output_tokens": 5000
        }
    )

def run_agent(user_message, profile, careers):
    career_text = "\n".join([
        f"- {c['career_name']}: {c['description']}" 
        for c in careers[:5]  # solo las 5 primeras carreras
    ])


    profile_text = {
        "intereses": profile.get("intereses", []),
        "habilidades_percibidas": profile.get("habilidades_percibidas", [])
    }

    full_prompt = f"""
{SYSTEM_PROMPT}

============================
MENSAJE DEL USUARIO
============================
{user_message}

============================
PERFIL ACTUAL (MEMORIA)
============================
{profile_text}

============================
CARRERAS DISPONIBLES
============================
{career_text}
"""

    

    try:
        response = model.generate_content(full_prompt)

        print("###########################################################################")
        print("Gemini response:", response)
        print("###########################################################################")

        if response.candidates:
            candidate = response.candidates[0]
            content_text = ""

            if hasattr(candidate, "content") and candidate.content:
                if hasattr(candidate.content, "parts"):
                    for part in candidate.content.parts:
                        if hasattr(part, "text") and part.text:
                            content_text += part.text
                elif hasattr(candidate.content, "text") and candidate.content.text:
                    content_text = candidate.content.text

            if content_text.strip():
                return content_text

        return "Error en Gemini: no se generó texto"

    except Exception as e:
        return f"Error en Gemini: {str(e)}"
