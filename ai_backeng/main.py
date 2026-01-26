# main.py

from fastapi import FastAPI
from pydantic import BaseModel

from ai_backeng.memory import empty_profile
from ai_backeng.agent import run_agent
from ai_backeng.embeddings.embed_user_text import build_user_embedding
from ai_backeng.matching.get_best_careers import get_best_careers

from ai_backeng.embeddings.blend import blend_embeddings
from ai_backeng.embeddings.embedding_provider import get_embedding

app = FastAPI()
USER_MEMORY = empty_profile()

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
def chat(input: ChatInput):
    # actualizar embedding acumulado
    USER_MEMORY["user_embedding"] = build_user_embedding(
        USER_MEMORY,
        input.message
    )

    careers = get_best_careers(
        USER_MEMORY["user_embedding"],
        USER_MEMORY["preferencias"]
    )

    reply = run_agent(
        input.message,
        USER_MEMORY,
        careers
    )

    return {"reply": reply}
