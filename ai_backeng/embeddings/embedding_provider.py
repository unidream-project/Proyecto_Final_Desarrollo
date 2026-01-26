from sentence_transformers import SentenceTransformer
import os

PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local-e5")

model = None
EMBEDDING_MODEL_NAME = None

if PROVIDER == "local-e5":
    model = SentenceTransformer("intfloat/multilingual-e5-large")
    EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large"

def get_embedding(text: str) -> list[float]:
    if model is None:
        raise RuntimeError("Embedding model not initialized")

    text = f"passage: {text}"
    embedding = model.encode(
        text,
        normalize_embeddings=True
    )
    return embedding.tolist()
