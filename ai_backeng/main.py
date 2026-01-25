from fastapi import FastAPI
from pydantic import BaseModel
from supabase_client import get_all_careers
from memory import empty_profile
from agent import run_agent

app = FastAPI()

# memoria temporal (demo)
USER_MEMORY = empty_profile()

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
def chat(input: ChatInput):
    careers = get_all_careers()

    reply = run_agent(
        input.message,
        USER_MEMORY,
        careers
    )

    return {
        "reply": reply,
        "memory": USER_MEMORY
    }
