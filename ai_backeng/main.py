from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- IMPORTANTE
from pydantic import BaseModel

from ai_backeng.db.postgres import init_db, get_pool
from ai_backeng.embeddings.embedding_provider import get_embedding
from ai_backeng.embeddings.blend import blend_embeddings
from ai_backeng.matching.get_best_careers import get_best_careers
from ai_backeng.agent import run_agent
from ai_backeng.memory import empty_profile

app = FastAPI()

# =========================
# CONFIGURACIÓN CORS (EL PUENTE)
# =========================
origins = [
    "http://localhost:5173",                 # Para cuando pruebas en tu PC
    "https://unidream.vercel.app",           # Tu frontend en producción
    "https://unidream-git-main-francocriollos-projects.vercel.app" # Preview deployments (opcional)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # Permitir GET, POST, OPTIONS, etc.
    allow_headers=["*"],    # Permitir enviar JSON, Tokens, etc.
)

@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# MODELOS
# =========================

class ChatInput(BaseModel):
    message: str


# =========================
# MEMORIA SIMPLE (ejemplo)
# =========================

USER_MEMORY = empty_profile()


# =========================
# STARTUP
# =========================

@app.on_event("startup")
async def startup():
    await init_db()


# =========================
# ENDPOINT
# =========================

@app.post("/chat")
async def chat(input: ChatInput):
    pool = await get_pool()

    new_emb = get_embedding(f"query: {input.message}")

    USER_MEMORY["user_embedding"] = blend_embeddings(
        USER_MEMORY.get("user_embedding"),
        new_emb
    )

    careers = await get_best_careers(
        pool,
        USER_MEMORY["user_embedding"],
        USER_MEMORY["preferencias"]
    )

    reply = run_agent(input.message, USER_MEMORY, careers)

    return {"reply": reply}
