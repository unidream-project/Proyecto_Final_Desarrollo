from fastapi import FastAPI
from pydantic import BaseModel

from ai_backeng.memory import empty_profile
from ai_backeng.agent import run_agent
from ai_backeng.embeddings.user_embedding import embed_user_text
from ai_backeng.matching.get_best_careers import get_best_careers

app = FastAPI()

USER_MEMORY = empty_profile()

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
def chat(input: ChatInput):
    user_embedding = embed_user_text(input.message)

    careers = get_best_careers(
        user_embedding,
        USER_MEMORY["preferencias"]
    )

    reply = run_agent(
        input.message,
        USER_MEMORY,
        careers
    )

    return {
        "reply": reply
    }
