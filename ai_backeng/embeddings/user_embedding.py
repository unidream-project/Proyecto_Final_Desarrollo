from ai_backeng.embeddings.embedding_provider import get_embedding

def embed_user_text(text: str) -> list[float]:
    text = f"query: {text}"
    return get_embedding(text)
