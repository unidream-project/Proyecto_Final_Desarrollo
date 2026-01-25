import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini")

# ======================
# GEMINI (ACTUAL)
# ======================

if PROVIDER == "gemini":
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def get_embedding(text: str) -> list[float]:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return result["embedding"]

    EMBEDDING_MODEL_NAME = "gemini-embedding-001"

# ======================
# FUTURO: OPENAI / OTROS
# ======================
# elif PROVIDER == "openai":
#     ...
